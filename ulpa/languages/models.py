from __future__ import unicode_literals, absolute_import

from django.db import models
from django.template.defaultfilters import slugify

from ulpa.utils.model_helpers import CreatedModifiedMixin
from ulpa.users.models import User
from openpyxl import load_workbook


class LanguageManager(models.Manager):
    def get_all_valid_languages(self):
        return self


class Language(CreatedModifiedMixin, models.Model):

    name = models.CharField(max_length=256, unique=True)
    alternative_name = models.CharField(max_length=256, blank=True)
    slug = models.SlugField(max_length=50)

    individual_language = models.TextField(max_length=512)

    description = models.TextField()

    categories = models.ManyToManyField('languages.LanguageCategory',
                                        related_name='languages',
                                        blank=True)

    how_widely_taught = models.CharField(max_length=256)

    abs_data = models.TextField(max_length=512, blank=True, null=True)
    abs_classification = models.CharField(null=True,
                                          blank=True,
                                          max_length=256)
    objects = LanguageManager()

    class Meta(object):
        ordering = ('name', )
        verbose_name = "language"
        verbose_name_plural = "languages"

    def __unicode__(self):
        return u'%s' % (self.name)


class LanguageCategory(CreatedModifiedMixin, models.Model):
    """

    """
    name = models.CharField(max_length=256, blank=True, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=50)

    class Meta(object):
        """

        """
        verbose_name = "language category"
        verbose_name_plural = "language categories"

    def __unicode__(self):
        return u'%s' % (self.name)


class LanguageBulkUpload(CreatedModifiedMixin, models.Model):
    MAX_UPLOAD_SIZE = 5*1024*1024  # 5MB
    STATUS_PENDING = 'pending'
    STATUS_PROCESSED = 'processed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSED, 'Processed'),
        (STATUS_CANCELLED, 'Cancelled'),
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                              default=STATUS_PENDING)
    user = models.ForeignKey(User, related_name="language_bulk_uploads",
                             null=True, blank=True, on_delete=models.SET_NULL)
    xlsx_file = models.FileField(upload_to='languages_bulk_uploads')

    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING

    @property
    def is_processed(self):
        return self.status == self.STATUS_PROCESSED

    @property
    def is_cancelled(self):
        return self.status == self.STATUS_CANCELLED

    @property
    def errors(self):
        errors = []

        for result in self.results:
            if result['errors']:
                errors.append(result['errors'])

        return errors

    def process(self):
        if self.status != self.STATUS_PENDING:
            return False

        if self.errors:
            return False

        records = self.save_records()

        self.status = self.STATUS_PENDING

        self.save()

        return records

    def save_records(self):
        records = {}
        category_records = set()
        language_records = set()

        for result in self.results:
            language_record = result['language']
            category_record = result['language_category']
            category_list = []

            if category_record:
                for id, category in category_record.iteritems():
                    try:
                        existing_category = LanguageCategory.objects.get(name=category.name)
                    except LanguageCategory.DoesNotExist:
                        existing_category = None

                    if existing_category:
                        category.pk = existing_category.pk
                        category.created = existing_category.created

                    category.slug = slugify(category.name)

                    category.save()
                    category_list.append(category.pk)
                    category_records.add(category)
                    records['categories'] = category_records

            if language_record:
                try:
                    existing_language = Language.objects.get(name=language_record.name)
                except Language.DoesNotExist:
                    existing_language = None

                if existing_language:
                    language_record.pk = existing_language.pk
                    language_record.created = existing_language.created

                language_record.slug = slugify(language_record.name)

                language_record.save()
                language_record.categories = category_list
                language_record.save()
                language_records.add(language_record)
                records['languages'] = language_records

        return records

    def cancel(self):
        if self.status != self.STATUS_PENDING:
            return False

        self.status = self.STATUS_CANCELLED
        self.save()

        return True

    @property
    def results(self):
        from .forms import LanguageFormForBulkUpload, LanguageCategoryFormForBulkUpload

        if hasattr(self, '_cached_results'):
            return self._cached_results

        results = []

        xlsx_size = self.xlsx_file._get_size()

        if xlsx_size > self.MAX_UPLOAD_SIZE:
            return results

        xlsx_workbook = load_workbook(self.xlsx_file.file)
        xlsx_sheet = xlsx_workbook.get_active_sheet()

        for index, row in enumerate(xlsx_sheet.rows):
            if index == 0:
                continue

            name = row[0].value
            alternative_name = row[1].value
            individual_language = row[2].value
            description = row[3].value
            how_widely_taught = row[4].value
            abs_data = row[5].value
            abs_classification = row[6].value
            category = row[7].value
            category_description = row[8].value

            categories = category.split(";")


            errors = []

            raw_data = {
                'name' : name,
                'alternative_name': alternative_name,
                'description': description,
                'individual_language' : individual_language,
                'how_widely_taught': how_widely_taught,
                'abs_data': abs_data,
                'abs_classification': abs_classification,
                'category': category,
                'category_description': category_description,
            }

            # TODO: Read below
            # If multiple categories within 'Language Category' column,
            # we need to ensure all the categories are inside the database.
            # The issue is, the language category description currently works for one category.
            # We need to create a loop through of the category list that checks each
            # new category against the database. Then create if necessary.

            category_dict = {}
            category_form_data_dict = {}
            categories_list = []
            
            for index, category in enumerate(categories):
                category = category.lstrip(' ')
                category_form_data_dict[index] = {
                    'name': category,
                    'description': category_description,
                }

                try:
                    language_category = LanguageCategory.objects.get(name=category)
                except LanguageCategory.DoesNotExist:
                    language_category = None

                if language_category:
                    categories_list.append(language_category.pk)

                category_form = LanguageCategoryFormForBulkUpload(category_form_data_dict[index], instance=language_category)

                if category_form.is_valid():
                    pass
                else:
                    for field, field_errors in category_form.errors.iteritems():
                        for error in field_errors:
                            message = u'%s - %s' % (LanguageCategoryFormForBulkUpload.FIELD_NAMES[field], error)
                            errors.append(message)

                if not errors:
                    category_dict[index] = category_form.save(commit=False)
                else:
                    category_dict[index] = None

            language_form_data = {
                'name' : name,
                'alternative_name': alternative_name,
                'description': description,
                'individual_language' : individual_language,
                'how_widely_taught': how_widely_taught,
                'abs_data': abs_data,
                'categories': categories_list,
                'abs_classification': abs_classification,
            }

            try:
                language = Language.objects.get(name=name)
            except Language.DoesNotExist:
                language = None

            language_form = LanguageFormForBulkUpload(language_form_data, instance=language)

            if language_form.is_valid():
                pass
            else:
                for field, field_errors in language_form.errors.iteritems():
                    for error in field_errors:
                        message = u'%s - %s' % (LanguageFormForBulkUpload.FIELD_NAMES[field], error)
                        errors.append(message)

            if not errors:
                language = language_form.save(commit=False)
            else:
                language = None

            result = {
                'raw_data': raw_data,
                'language_form_data': language_form_data,
                'category_form_data': category_form_data_dict,
                'language': language,
                'language_category': category_dict,
                'errors': errors,
            }

            results.append(result)

        self._cached_results = results

        return results
