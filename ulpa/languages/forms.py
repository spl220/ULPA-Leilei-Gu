from django import forms

from ulpa.universities.models import University
from ulpa.subjects.models import Subject
from ulpa.utils.form_helpers import ModelForm, BaseBulkUploadForm

from .models import Language, LanguageCategory, LanguageBulkUpload


class LanguageSearchForm(forms.Form):

    language = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        label='Language',
        required=True,
        to_field_name="name"
    )
    university = forms.ModelMultipleChoiceField(
        queryset=University.objects.all(),
        to_field_name="name",
        required=False
    )
    study_choice = forms.ChoiceField(
        choices=Subject.STUDY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    intensity = forms.MultipleChoiceField(
        choices=Subject.INTENSITY_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )

    sort_by = forms.CharField(
        widget=forms.HiddenInput(),
        initial='language')

    def clean(self):
        cleaned_data = super(LanguageSearchForm, self).clean()
        language = cleaned_data.get('language')
        university = cleaned_data.get('university')
        study_choice = cleaned_data.get('study_choice')
        intensity = cleaned_data.get('intensity')

        return cleaned_data


class LanguagesBulkUploadForm(BaseBulkUploadForm):
    """
    Form to import XLSX file containing new and updated subjects
    """

    class Meta:
        model = LanguageBulkUpload
        fields = ('xlsx_file',)


class LanguageFormForBulkUpload(ModelForm):

    FIELD_NAMES = {
        'name': 'Name',
        'alternative_name': 'Alternative Name',
        'categories': 'Language Category',
        'description': 'Language Description',
        'individual_language': 'Individual Language Page',
        'how_widely_taught': 'How Widely Taught',
        'abs_data': 'ABS Census Data',
        'abs_classification': 'ABS Australian Standard Classification of Languages',
    }

    class Meta:
        model = Language
        fields = ('name', 'alternative_name', 'categories', 'description', 'individual_language', 'how_widely_taught',
                  'abs_data', 'abs_classification')

class LanguageCategoryFormForBulkUpload(ModelForm):

    FIELD_NAMES = {
        'name': 'Language Category Name',
        'description': 'Language Category Description',
    }

    class Meta:
        model = LanguageCategory
        fields = ('name', 'description')
