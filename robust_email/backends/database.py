from robust_email import settings
from robust_email.models import EmailMessage
import time


class DatabaseBackend(settings.BASE_EMAIL_BACKEND):
    def send_messages_old(self, email_messages):
        email_objects = []
        for message in email_messages:
            obj, created = \
                EmailMessage.objects.get_or_create_for_message(message)
            email_objects.append(obj)
        email_messages = [obj.to_message() for obj in email_objects]
        return super(DatabaseBackend, self).send_messages(email_messages)

    def send_messages(self, email_messages):
        for email_message in email_messages:
            self._send(email_message)
                
    def _send(self, email_message):
        """ Send the email and save to database. """
        if not email_message.recipients():
            return False

        if not hasattr(email_message, 'robust_object'):
            obj, created = EmailMessage.objects.get_or_create_for_message(email_message)

        fail_silently = self.fail_silently  # backup real value
        self.fail_silently = False  # we want to know about exceptions
        try:
            assert hasattr(email_message, 'robust_object')
            super(DatabaseBackend, self).send_messages([email_message])
        except Exception as e:
            try:
                # Sleep to avoid race conditions if we've been asked to
                # TODO: Make this a bit more robust
                if hasattr(email_message.robust_object, 'sleep_before_log'):
                    time.sleep(email_message.robust_object.sleep_before_log)

                email_message.robust_object.log_failure(e)
            except AttributeError:
                pass  # no robust_object!?
            if not fail_silently:  # check real value
                raise
            return False
        else:
            # Sleep to avoid race conditions if we've been asked to
            # TODO: Make this a bit more robust
            if hasattr(email_message.robust_object, 'sleep_before_log'):
                time.sleep(email_message.robust_object.sleep_before_log)

            email_message.robust_object.log_success()
            return True
        finally:
            self.fail_silently = fail_silently  # restore real value