from django.apps import AppConfig
from django.db.models.signals import post_save


default_app_config = 'robust_email.RobustEmailConfig'


def email_message_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        instance.post_creation()


class RobustEmailConfig(AppConfig):
    name = 'robust_email'

    def ready(self):
        from .models import EmailMessage
        
        post_save.connect(email_message_post_save, EmailMessage,
                  dispatch_uid="robust_email.signals")
            
