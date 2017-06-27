from django import template
from robust_email import settings

register = template.Library()

@register.simple_tag
def view_email_online_url():
    return settings.VIEW_EMAIL_ONLINE_URL_PLACEHOLDER