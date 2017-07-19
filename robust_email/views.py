from django.http import HttpResponse, Http404
from robust_email.models import EmailMessage
from robust_email.util import get_token
from django.contrib import messages
from django.shortcuts import redirect

def view_email(request, message_id, token):
    try:
        message = EmailMessage.objects.get(pk=message_id)
        assert token == get_token(message, 'view')
        html = message.get_html() or message.body # fallback gracefully
        return HttpResponse(html)
    except (EmailMessage.DoesNotExist, AssertionError):
        raise Http404