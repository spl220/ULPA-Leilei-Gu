import datetime

from django.core.exceptions import ValidationError
from django.db import models



class CreatedModifiedMixin(models.Model):
    created = models.DateTimeField(verbose_name="Date created", auto_now_add=True, help_text="The date and time at which the object was entered into the system")
    modified = models.DateTimeField(verbose_name="Date last modified", auto_now=True, help_text="The date and time at which the object was last modified")

    class Meta:
        abstract = True


def validate_date_after_1900(value):
    if value < datetime.date(1900, 1, 1):
        raise ValidationError('This date cannot be prior to January 1, 1900')
