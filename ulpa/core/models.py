from django.db import models
from django.contrib.sites.models import Site

from ulpa.utils.model_helpers import CreatedModifiedMixin


class SiteConfigurationManager(models.Manager):
    def get_current(self):
        active_configurations = self.filter(active=True).order_by('-created')

        if active_configurations:
            return active_configurations[0]

        return None


class SiteConfiguration(CreatedModifiedMixin, models.Model):
    active = models.BooleanField(default=False, help_text="If ticked, the settings in this configuration will become live.")
    name = models.CharField(max_length=255, help_text="A name for this collection. For reference only.")

    # General Site Details
    creative_commons_statement = models.TextField(null=True, blank=True, help_text="The site creative commons notice, displayed in the footer")
    copyright_statement = models.TextField(null=True, blank=True, help_text='The site copyright statement, displayed in the footer', max_length=50)
    liability_statement = models.TextField(null=True, blank=True, help_text="The site liability notice, displayed in the footer")
    privacy_policy = models.TextField(null=True, blank=True, help_text="The site privacy policy, displayed in the footer")
    disclaimer_statement = models.TextField(null=True, blank=True, help_text="The site disclaimer notice, displayed in the footer")
    terms_of_use_statement = models.TextField(null=True, blank=True, help_text="The site terms of use, displayed in the footer")
    page_not_found_content = models.TextField(null=True, blank=True, help_text="The copy text that appears on the 404 page")

    # Home Page
    home_page_heading = models.CharField(max_length=255, null=True, blank=True, help_text="The heading that appears above the textual content on the home page")
    home_page_content = models.TextField(null=True, blank=True, help_text="The textual content that appears at the top of the home page")

    # About page
    about_page_heading = models.CharField(max_length=255, null=True, blank=True, help_text="The heading that appears above the textual content on the about page")
    about_page_content = models.TextField(null=True, blank=True, help_text="The textual content that appears at the top of the about page")

    # Study at other University page
    other_university_heading = models.CharField(max_length=255, null=True, blank=True, help_text="The heading that appears above the textual content on the resources page")
    other_university_content = models.TextField(null=True, blank=True, help_text="The textual content that appears at the top of the resources page")

    # Where can I study Indigenous Languages page
    where_can_study_indigenous_languages_heading = models.CharField(max_length=255, null=True, blank=True, help_text="The heading that appears above the textual content on the register interest page")
    where_can_study_indigenous_languages_content = models.TextField(null=True, blank=True, help_text="The textual content that appears at the top of the register interest page")

    # What languages can I study page
    what_languages_can_study_heading = models.CharField(max_length=255, null=True, blank=True, help_text="The heading that appears above the textual content on the register interest page")
    what_languages_can_study_content = models.TextField(null=True, blank=True, help_text="The textual content that appears at the top of the register interest page")

    # Why study languages page
    why_study_languages_heading = models.CharField(max_length=255, null=True, blank=True, help_text="The heading that appears above the textual content on the register interest page")
    why_study_languages_content = models.TextField(null=True, blank=True, help_text="The textual content that appears at the top of the register interest page")

    # Facebook information
    facebook_url = models.URLField(null=True, blank=True)
    facebook_title = models.CharField(max_length=256, null=True, blank=True)
    facebook_description = models.TextField(null=True, blank=True)
    facebook_image = models.ImageField(null=True, blank=True)

    objects = SiteConfigurationManager()

    class Meta(object):
        ordering = ['name',]

    def __unicode__(self):
        return u'%s' % self.name
