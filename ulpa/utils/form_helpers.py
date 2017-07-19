from django import forms
from django.forms.fields import FileField
from django.core.exceptions import ValidationError


class BaseBulkUploadForm(forms.ModelForm):
    MAX_UPLOAD_SIZE = 5*1024*1024  # 5MB
    MAX_RECORDS = 200

    def clean_xlsx_file(self):
        post_xlsx_file = self.files['xlsx_file']

        return post_xlsx_file


class BaseForm(object):
    """
    Strips whitespace
    """
    def _clean_fields(self):
        for name, field in self.fields.items():
            # value_from_datadict() gets the data from the data dictionaries.
            # Each widget type knows how to retrieve its own data, because some
            # widgets split data over several HTML fields.
            value = field.widget.value_from_datadict(self.data, self.files,
                                                     self.add_prefix(name))

            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    if isinstance(value, basestring):
                        value = field.clean(value.strip())
                    else:
                        value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError, e:
                self._errors[name] = self.error_class(e.messages)
                if name in self.cleaned_data:
                    del self.cleaned_data[name]


class Form(BaseForm, forms.Form):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)


class ModelForm(BaseForm, forms.ModelForm):
    pass
