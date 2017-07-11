import warnings

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.template import RequestContext
from django.conf import settings
from pynliner import fromString as inline_html

from robust_email.models import EmailMessage



def send_html_email(recipient, subject_template, content_template, context, attachments=None):
    if attachments is None:
        attachments = []

    # If the recipient is a user, grab their email address, otherwise assume
    # the address has been provided directly
    User = get_user_model()

    if isinstance(recipient, User):
        email = recipient.email
        user = recipient
    else:
        email = recipient
        user = None

    if not email:
        return

    # Grab the default email address from settings
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@ulpa.edu.au')

    # Grab the base url for fully qualified links
    current_site = Site.objects.get_current()
    base_url = ''.join(['http://', current_site.domain])

    # Construct the subject
    subject = render_to_string(subject_template, context).rstrip()

    # Do an initial save on the email message. (So that we have a message URL to
    # include in the actual email)
    message = EmailMessage.objects.create(
        to=email,
        user=user,
        from_email=from_email,
        subject=subject,
        body="",
    )

    # Construct the message url
    message_url = base_url + message.get_absolute_url()

    # Plain text content of the email is just a link to view online
    # TODO: Allow for plain text templates
    text_content = "Having trouble seeing this message? View it in your browser at %s" % message_url

    # Save the body of the message into the object
    message.body = text_content
    message.save()

    message.sleep_before_log = 2

    # Construct the HTML content
    context['site'] = current_site
    context['base_url'] = base_url
    context['message_url'] = message_url
    context['subject'] = subject
    context['STATIC_URL'] = getattr(settings, 'STATIC_URL', "")
    context['user'] = recipient

    html_content = render_to_string(content_template, context)

    # Convert the html content to inline styles so that it renders properly in gmail
    # Ignore deprecation warnings because of a really stupid one built into cssutils
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        html_content = inline_html(html_content)

    # Save the HTML content in as an attachment
    message.alternativecontent_set.create(
        content=html_content,
        mimetype="text/html",
    )

    for (attachment, mimetype) in attachments:
        message.attachment_set.create(
            content=attachment,
            mimetype=mimetype,
        )

    # Send the message
    message.send(fail_silently=True, non_blocking=True)
