from django import forms


class LanguageSearchForm(forms.Form):
    language = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Language', max_length=100)

EMAIL = 'Email'
PHONE = 'Phone'

contact_choices = (
    (EMAIL, 'Email'),
    (PHONE, 'Phone'),
)


class ContactForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    contact_number = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    preferred_contact_method = forms.ChoiceField(choices=contact_choices)
    your_message = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        contact_number = cleaned_data.get('contact_number')
        email = cleaned_data.get('email')
        preferred_contact_method = cleaned_data.get('preferred_contact_method')


class URLCheckForm(forms.Form):
    run_check = forms.CharField(label='reset', max_length=256, widget=forms.HiddenInput(), initial='GO')