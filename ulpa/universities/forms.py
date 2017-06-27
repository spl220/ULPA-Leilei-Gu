from django import forms

from ulpa.subjects.models import Subject
from ulpa.languages.models import Language
from ulpa.utils.form_helpers import ModelForm, BaseBulkUploadForm

from .models import University, UniversityBulkUpload


class UniversitySearchForm(forms.Form):

    language = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        label='Language',
        required=False,
        to_field_name="name"
    )
    university = forms.ModelMultipleChoiceField(
        queryset=University.objects.all(),
        required=True,
        to_field_name="name"
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
        initial='university')

    def clean(self):
        cleaned_data = super(UniversitySearchForm, self).clean()
        language = cleaned_data.get('language')
        university = cleaned_data.get('university')
        study_choice = cleaned_data.get('study_choice')
        intensity = cleaned_data.get('intensity')

        return cleaned_data

class UniversityBulkUploadForm(BaseBulkUploadForm):
    """
    Form to import XLSX file containing new and updated subjects
    """

    class Meta:
        model = UniversityBulkUpload
        fields = ('xlsx_file',)


class UniversityFormForBulkUpload(ModelForm):

    FIELD_NAMES = {
        'name': 'Name',
        'url': 'Main URL',
        'cross_institutional_url': 'Cross Institutional URL',
    }

    class Meta:
        model = University
        fields = ('name', 'url', 'cross_institutional_url')
