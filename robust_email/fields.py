from django.db import models



class EmailListField(models.TextField):
    """ Model field for storing list of email addresses.

    Stored as comma-separated list. Email address validation is not currently
    performed, and "Bob <bob@example.com>, Alice <alice@example.com>" should
    work OK. Might need to look into handling embedded commas in recipient
    names.
    """

    description = "A comma-separated list of email addresses"
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        if not 'help_text' in kwargs:
            kwargs['help_text'] = 'Comma-separated list of email addresses'
        super(EmailListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
            
        if type(value) == list:
            return value
        try:
            return value.split(',')
        except:
            raise exceptions.ValidationError('Not comma-separated string')

    def get_prep_value(self, value):
        return super(EmailListField, self).get_prep_value(','.join(value))

try:
    # tell south to treat EmailListField as a TextField
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^robust_email\.fields\.EmailListField"])
except ImportError:
    # south not installed, nevermind
    pass
