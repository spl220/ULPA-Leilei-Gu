from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from robust_email.helpers import send_html_email


def contact_form_sent_handler(form, **kwargs):
    # TODO SET EMAIL
    email_recipients = getattr(settings, "EMAIL_RECIPIENTS", [])

    current_site = Site.objects.get_current()
    first_name = form.data.get('first_name')
    last_name = form.data.get('last_name')
    contact_number = form.data.get('contact_number')
    email = form.data.get('email')
    preferred_contact_method = form.data.get('preferred_contact_method')
    your_message = form.data.get('your_message')

    subject_template = "core/emails/contact_form_subject.html"
    content_template = "core/emails/contact_form_content.html"

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'contact_number': contact_number,
        'email': email,
        'preferred_contact_method': preferred_contact_method,
        'your_message': your_message,
        'current_site': current_site,
    }

    send_html_email(email_recipients, subject_template, content_template, context)
