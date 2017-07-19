from django.contrib import admin
from .models import SiteConfiguration

class SiteConfigurationAdmin(admin.ModelAdmin):
    model = SiteConfiguration

    fieldsets = (
        (None, {
            'fields': ['name', 'active', ]
        }),
        ('General Site Details', {
            'fields': [
                'creative_commons_statement',
                'copyright_statement',
                'liability_statement',
                'privacy_policy',
                'disclaimer_statement',
                'terms_of_use_statement',
                'page_not_found_content',
            ]
        }),
        ('Home Page', {
            'fields': [
                'home_page_heading',
                'home_page_content',
            ]
        }),
        ('About Page', {
            'fields': [
                'about_page_heading',
                'about_page_content',
            ]
        }),
        ('Study At Other University Page', {
            'fields': [
                'other_university_heading',
                'other_university_content',
            ]
        }),
        ('Where Can I Study Indigenous Languages Page', {
            'fields': [
                'where_can_study_indigenous_languages_heading',
                'where_can_study_indigenous_languages_content',
            ]
        }),
        ('What Languages Can I Study Page', {
            'fields': [
                'what_languages_can_study_heading',
                'what_languages_can_study_content',
            ]
        }),
        ('Why Study Languages Page', {
            'fields': [
                'why_study_languages_heading',
                'why_study_languages_content',
            ]
        }),
        ('Facebook Share Information', {
            'fields': [
                'facebook_title',
                'facebook_description',
                'facebook_url',
                'facebook_image',
            ]
        }),
    )

    list_display = ['name', 'pk', 'created', 'created', 'modified', 'active']

admin.site.register(SiteConfiguration, SiteConfigurationAdmin)
