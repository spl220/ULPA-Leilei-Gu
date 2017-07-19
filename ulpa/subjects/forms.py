import csv

from django import forms
from django.core.files import File

from .models import Subject, SubjectBulkUpload
from ulpa.utils.form_helpers import ModelForm, BaseBulkUploadForm


class SubjectSearchForm(forms.Form):
    """
    Search form to look up appropriate subjects
    """
    q = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                        label='Search for Subject',
                        max_length=100)


class SubjectsBulkUploadForm(BaseBulkUploadForm):
    """
    Form to import XLSX file containing new and updated subjects
    """

    class Meta:
        model = SubjectBulkUpload
        fields = ('xlsx_file',)


class SubjectFormForBulkUpload(ModelForm):
    FIELD_NAMES = {
        'title': 'Title',
        'state': 'State',
        'code': 'Code',
        'url': 'URL',
        'university': 'University',
        'other_university': 'Other University',
        'intensity': 'Intensity',
        'language': 'Language',
        'prerequisite': 'Prerequisite Language',
        'non_beginner_level_available': 'Non Beginner Level Available',
        'next_offered': 'Next Offered',
        'study_choice': 'Study Choice',
        'notes': 'Notes',
    }

    class Meta:
        model = Subject
        fields = ('title', 'state', 'code', 'url', 'university', 'other_university',
                  'intensity', 'language', 'prerequisite',
                  'non_beginner_level_available', 'next_offered',
                  'study_choice', 'notes',)
