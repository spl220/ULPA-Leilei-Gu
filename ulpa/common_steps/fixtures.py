"""

"""
from lettuce import before
from django.core.management import call_command


@before.all
def load_initial_fixtures():
    """

    """
    call_command('loaddata', '001_initial', app='universities')
    call_command('loaddata', '001_initial', app='languages')
    call_command('loaddata', '001_initial', app='subjects')
    call_command('loaddata', '001_initial', app='core')
    call_command('loaddata', '001_initial', app='faqs')
