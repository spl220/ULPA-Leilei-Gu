"""
Outlines the classes used in the 'universities' modules
"""

from __future__ import unicode_literals, absolute_import
import httplib
import urllib
import urllib2

from django.db import models

from openpyxl import load_workbook

from ulpa.utils.model_helpers import CreatedModifiedMixin
from ulpa.users.models import User


class University(CreatedModifiedMixin, models.Model):
    """
    A single University
    """

    name = models.CharField(max_length=256)

    url = models.URLField(blank=True)
    cross_institutional_url = models.URLField(blank=True)

    logo = models.ImageField(blank=True, help_text='Max size: 120px x 40px')

    class Meta(object):
        ordering = ('name', )
        verbose_name = "university"
        verbose_name_plural = "universities"

    def __unicode__(self):
        return u'%s' % (self.name)


def check_url():
    url_report = {}
    url_status = ''
    cross_institutional_url_status = ''

    universities = University.objects.all()

    for university in universities:
        if university.url:
            try:
                url_status = urllib2.urlopen(university.url, timeout=3).getcode()
            except Exception, e:
                url_status = "The following error occured: %s" % e
        else:
            url_status = "No URL Found"
        if university.cross_institutional_url:
            try:
                cross_institutional_url_status = urllib.urlopen(university.cross_institutional_url).getcode()
            except Exception, e:
                cross_institutional_url_status = "The following error occured: %s" % e   
        else:
            cross_institutional_url_status = "No Cross Institutional URL Found"

        url_report[university.name] = {'url_status': url_status, 'cross_institutional_url_status': cross_institutional_url_status}

    return url_report


class UniversityBulkUpload(CreatedModifiedMixin, models.Model):
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
    user = models.ForeignKey(User, related_name="university_bulk_uploads",
                             null=True, blank=True, on_delete=models.SET_NULL)
    xlsx_file = models.FileField(upload_to='university_bulk_uploads')

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
        records = []

        for result in self.results:
            record = result['university']

            if record:
                record.bulk_upload = self
                record.save()
                records.append(record)

        return records

    def cancel(self):
        if self.status != self.STATUS_PENDING:
            return False

        self.status = self.STATUS_CANCELLED
        self.save()

        return True

    @property
    def results(self):
        from .forms import UniversityFormForBulkUpload

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
            url = row[1].value
            cross_institutional_url = row[2].value

            errors = []

            try:
                university = University.objects.get(name=name)
            except University.DoesNotExist:
                university = None
            except University.MultipleObjectsReturned:
                university = University.objects.filter(name=name)
                university = university[0]

            raw_data = {
                'name': name,
                'url': url,
                'cross_institutional_url': cross_institutional_url,
            }

            form_data = {
                'name': name,
                'url': url,
                'cross_institutional_url': cross_institutional_url,
            }

            form = UniversityFormForBulkUpload(form_data, instance=university)

            if form.is_valid():
                pass
            else:
                for field, field_errors in form.errors.iteritems():
                    for error in field_errors:
                        message = u'%s - %s' % (UniversityFormForBulkUpload.FIELD_NAMES[field], error)
                        errors.append(message)

            if not errors:
                university = form.save(commit=False)
            else:
                university = None

            result = {
                'raw_data': raw_data,
                'form_data': form_data,
                'university': university,
                'errors': errors,
            }

            results.append(result)

        self._cached_results = results

        return results
