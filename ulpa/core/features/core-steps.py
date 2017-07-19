from lettuce import (
    after,
    before,
    step,
    world,
)
from selenium import webdriver

# from django.conf import settings
# from django.core.wsgi import get_wsgi_application
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
# application = get_wsgi_application()
from lettuce.django.steps.models import (creates_models,
                                         reset_sequence,
                                         hashes_data)
from lettuce_webdriver.webdriver import *
from ulpa.universities.models import University
from ulpa.common_steps.fixtures import *


@before.all
def setup_browser():
    world.browser = webdriver.Firefox()


@creates_models(University)
def create_university(step):
    data = hashes_data(step)
    for row in data:
        university = University.objects.create(**row)
        university.save()

    reset_sequence(University)


@step(r'I go to the url (.*)')
def go_to_url(step, url):
    world.browser.get(url)


@after.all
def close_browser(total):
    world.browser.quit()