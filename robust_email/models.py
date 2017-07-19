import os

from django.db import models
from django.core import exceptions
from django.core import mail
from django.conf import settings
import robust_email.settings
from robust_email.fields import EmailListField
from robust_email.util import exception_class_string, get_token
from django import forms
import smtplib
import socket


NETWORK_ISSUES = (
    socket.error,
    smtplib.SMTPServerDisconnected,
    smtplib.SMTPConnectError,
    smtplib.SMTPHeloError,
    )
CONFIGURATION_ISSUES = (
    smtplib.SMTPAuthenticationError,
    smtplib.SMTPSenderRefused,
    )
TERMINAL_ISSUES = (
    smtplib.SMTPDataError, # e.g. No valid recipients
    smtplib.SMTPRecipientsRefused,
    )
TERMINAL_ISSUE_STRINGS = [exception_class_string(i) for i in TERMINAL_ISSUES]


class EmailMessageManager(models.Manager):
    def get_or_create_for_message(self, email_message):
        try:
            return (email_message.robust_object, False)
        except AttributeError:
            # create new
            obj = EmailMessage(message=email_message)
            obj.save()
            setattr(email_message,'robust_object', obj)
            return (obj, True)

    def get_successful(self):
        return self.filter(emailtransaction__exception_type='').distinct()

    def get_terminal(self):
        return self.filter(
            emailtransaction__exception_type__in=TERMINAL_ISSUE_STRINGS)

    def get_resendable(self):
        return self.exclude(emailtransaction__exception_type='').exclude(
            emailtransaction__exception_type__in=TERMINAL_ISSUE_STRINGS)

        
class EmailMessage(models.Model):
    """ A model for storing email messages.

    Most fields use TextField rather than imposing a max_length using a
    CharField since RFC2822 Section 2.1.1 indicates that no fixed limits
    apply to content, even subject lines.
    """
    
    to = EmailListField(blank=True)
    from_email = models.EmailField(blank=True)
    bcc = EmailListField(blank=True)
    
    subject = models.TextField(blank=True)
    body = models.TextField(blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="email_messages")

    created = models.DateTimeField(auto_now_add=True)

    # TODO:
    # - extra_headers
    # - attachments

    objects = EmailMessageManager()

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
    
    def __unicode__(self):
        return '"%s" to %s (%s)' % (self.subject, self.to_address_string(),
                                  self.created)
    @models.permalink
    def get_absolute_url(self):
        return ('view_email',
                [str(self.id), get_token(self, 'view')])
 
    def attempts(self):
        return self.emailtransaction_set.count()
        
    def successful(self):
        return self.emailtransaction_set.filter(exception_type='').exists()
    successful.boolean = True
    
    def _replace_placeholders(self, content):
        mapping = {
            (r'%s' % robust_email.settings.VIEW_EMAIL_ONLINE_URL_PLACEHOLDER):
                self.get_absolute_url(),
            }
        for placeholder, replacement in mapping.items():
            content = content.replace(placeholder, replacement)
        return content

    def replace_placeholders(self):
        self.body = self._replace_placeholders(self.body)
        self.save()
        for alternative in self.alternativecontent_set.all():
            alternative.content = self._replace_placeholders(
                alternative.content)
            alternative.save()

    def save_alternatives(self):
        for alternative in self.unsaved_alternative_content:
            alternative.email = self
            alternative.save()

    def post_creation(self):
        self.save_alternatives()
        self.replace_placeholders()
        
    def get_html(self):
        try:
            html = self.alternativecontent_set.get(mimetype='text/html')
        except:
            return None
        else:
            return html.content
            
    def to_address_string(self):
        if self.to in ([], [u'']):
            return 'NO DIRECT RECIPIENTS'
        else:
            return ', '.join(self.to)
    to_address_string.short_description = 'To'
    
    def __init__(self, *args, **kwargs):
        message = kwargs.pop('message', None)
        super(EmailMessage, self).__init__(*args, **kwargs)
        self.unsaved_alternative_content = []
        if message:
            if not isinstance(message, mail.EmailMessage):
                raise TypeError("robust_email.models.EmailMessage must be "
                                "initialised with a "
                                "django.core.mail.EmailMessage object, "
                                "not a %r" % message)
            self.from_message(message)

    def from_message(self, message):
        """ Initialise from django.core.mail.EmailMessage or subclass. """
        self.to = message.to
        self.from_email = message.from_email
        self.bcc = message.bcc
        self.subject = message.subject
        self.body = message.body
        if hasattr(message, 'alternatives'):
            for content, mimetype in message.alternatives:
                self.unsaved_alternative_content.append(AlternativeContent(
                        content=content, mimetype=mimetype))
        # TODO:
        # - extra_headers
        # - attachments

    def has_alternative_content(self):
        return (self.alternativecontent_set.count() > 0)

    def _kwargs(self):
        return {
            'subject': self.subject,
            'body': self.body,
            'from_email': self.from_email,
            'to': self.to,
            'bcc': self.bcc,
            }
                                    
    def to_message(self, connection=None):
        """ Create a django.core.mail.EmailMessage from self. """
        assert self.pk, "to_message can only be called on saved EmailMessages"
        kwargs = self._kwargs()
        kwargs['connection'] = connection
        if self.has_alternative_content():
            message = mail.EmailMultiAlternatives(**kwargs)
            for alternative_content in self.alternativecontent_set.all():
                message.attach_alternative(alternative_content.content,
                                           alternative_content.mimetype)

            for attachment in self.attachment_set.all():
                if attachment.content:
                    message.attach(attachment.filename, attachment.content.read(), attachment.mimetype)
        else:
            message = mail.EmailMessage(**kwargs)
        setattr(message, 'robust_object', self) # attach backreference
        return message

    def send(self, non_blocking=False, connection=None, fail_silently=False):
        message = self.to_message(connection=connection)
        if non_blocking:
            import threading
            t = threading.Thread(target=message.send)
            t.setDaemon(True)
            t.start()
            return None
        else:
            return message.send(fail_silently=fail_silently)
    
    def log_success(self):
        EmailTransaction.objects.create(email=self)

    def log_failure(self, exception):
        EmailTransaction.objects.create(email=self, exception=exception)

    def recipients(self):
        return self.to + self.bcc

    def cannot_send(self):
        return self.emailtransaction_set.filter(
            exception_type__in=TERMINAL_ISSUE_STRINGS).exists()
    cannot_send.boolean = True
    

class AlternativeContent(models.Model):
    """ A model for storing alternative email content. """
    email = models.ForeignKey(EmailMessage)
    content = models.TextField(blank=True)
    mimetype = models.CharField(max_length=255, help_text='e.g. text/html')

    def __unicode__(self):
        return 'Alternative %s content' % self.mimetype


class Attachment(models.Model):
    """ A model for storing attachments. """
    email = models.ForeignKey(EmailMessage)
    content = models.FileField(upload_to="email_attachments", null=True, blank=True)
    mimetype = models.CharField(max_length=255, help_text='e.g. text/html')

    def __unicode__(self):
        return 'Attachment (%s)' % self.mimetype

    @property
    def filename(self):
        if not self.content:
            return ''

        return os.path.basename(self.content.name)

    
class EmailTransaction(models.Model):
    email = models.ForeignKey(EmailMessage)
    exception_type = models.CharField(max_length=255, blank=True)
    exception_value = models.CharField(max_length=1024, blank=True)
    when = models.DateTimeField(auto_now_add=True, editable=True)

    class Meta:
        ordering = ['-when']
        get_latest_by = 'when'

    def __unicode__(self):
        if self.success():
            return 'Successful send at %s' % self.when
        else:
            return 'Failed send attempt at %s' % self.when
        
    def __init__(self, *args, **kwargs):
        exception = kwargs.pop('exception', None)
        super(EmailTransaction, self).__init__(*args, **kwargs)
        if exception:
            self.set_exception(exception)

    def set_exception(self, exception):
        self.exception_type = exception_class_string(exception.__class__)
        self.exception_value = str(exception)

    def terminal_error(self):
        return (self.exception_type in TERMINAL_ISSUE_STRINGS)
    terminal_error.boolean = True
            
    def success(self):
        return (self.exception_type == '')
    success.boolean = True
