from django.core.management.base import BaseCommand
from django.core import mail
from robust_email.models import EmailMessage, NETWORK_ISSUES
import sys

class Command(BaseCommand):
    help = "Send any non-terminally failed emails. "
    
    def handle(self, *args, **kwargs):
        resendable = EmailMessage.objects.get_resendable()
        print "%d emails to be sent" % len(resendable)
        if len(resendable) == 0:
            return
        sent = 0
        connection = mail.get_connection()
        connection.open()
        try:
            for index, message in enumerate(resendable):
                print "Sending message #", index+1, "...",
                sys.stdout.flush()
                try:
                    if message.send(connection=connection):
                        sent += 1
                        print "OK"
                    else:
                        print "failed?"
                except NETWORK_ISSUES:
                    print "Connection closed; aborting..."
                    break
                except Exception as e:
                    print "failed:", e
        finally:
            try:
                connection.close()
            except:
                pass # nevermind
            print "Sent: %d" % sent