"""
Models class for Subjects and SubjectBulkUploads.
Stores the Subject pre and post processing from the XLSX file
uploaded via the "subjects/import.html" page.
"""

from __future__ import unicode_literals, absolute_import
import ssl
# import threading
# import Queue
# import requests
import csv
import time
import httplib
import urllib
import urllib2
from django.core.files import File

from django.db import models

from openpyxl import load_workbook
from select_multiple_field.models import SelectMultipleField

from ulpa.users.models import User

from ulpa.utils.model_helpers import CreatedModifiedMixin


class Subject(CreatedModifiedMixin, models.Model):
    """
    A single Subject, related to universities and languages.

        A University has many Subjects and a Subject
        only exists in one University.

        A Language has many Subjects and a Subject
        only has one language.

    """

    VICTORIA = 'VIC'
    NEW_SOUTH_WALES = 'NSW'
    SOUTH_AUSTRALIA = 'SA'
    QUEENSLAND = 'QLD'
    WESTERN_AUSTRALIA = 'WA'
    TASMANIA = 'TAS'
    AUSTRALIAN_CAPITAL_TERRITORY = 'ACT'
    NORTHERN_TERRITORY = 'NT'

    STATE_CHOICES = (
        (VICTORIA, 'Victoria'),
        (NEW_SOUTH_WALES, 'New South Wales'),
        (SOUTH_AUSTRALIA, 'South Australia'),
        (QUEENSLAND, 'Queensland'),
        (WESTERN_AUSTRALIA, 'Western Australia'),
        (TASMANIA, 'Tasmania'),
        (AUSTRALIAN_CAPITAL_TERRITORY, 'Australian Capital Territory'),
        (NORTHERN_TERRITORY, 'Northern Territory'),
    )

    INTENSIVE = 'I'
    REGULAR = 'R'

    INTENSIVE_TEXT = 'intensive'
    REGULAR_TEXT = 'regular'
    REGULAR_AND_INTENSIVE = 'both'

    INTENSITY_CHOICES = (
        (INTENSIVE_TEXT, 'I want to do an intensive course (eg. summer school)'),
        (REGULAR_TEXT, 'I want to study over a regular semester'),
    )

    FACE_TO_FACE = 'on-campus'
    ONLINE = 'online'
    ALTONLINE = 'on-line'
    BOTH = 'both'

    YES = 'Yes'
    NO = 'No'
    NONE = 'None'

    STUDY_CHOICES = (
        (FACE_TO_FACE, "I want to study on-campus (but don't mind if a small portion is online)"),
        (ONLINE, 'I want to study entirely online'),
    )

    title = models.CharField(
        max_length=256
    )
    code = models.CharField(
        max_length=256
    )
    url = models.URLField(
        blank=True
    )

    university = models.ForeignKey(
        'universities.University',
        related_name='subjects',
        max_length=256
    )

    state = models.CharField(
        max_length=256,
        choices=STATE_CHOICES,
    )

    other_university = models.TextField(
        max_length=512,
        blank=True,
        null=True
    )

    intensity = SelectMultipleField(
        max_length=50,
        choices=INTENSITY_CHOICES,
    )

    language = models.ForeignKey(
        'languages.Language',
        related_name='subjects',
        max_length=256,
    )

    prerequisite = models.TextField(
        max_length=512,
        blank=True,
        null=True
    )

    non_beginner_level_available = models.BooleanField(
        default=False
    )

    next_offered = models.TextField(
        blank=True,
        null=True,
    )

    study_choice = SelectMultipleField(
        max_length=256,
        choices=STUDY_CHOICES
    )

    notes = models.TextField(
        blank=True
    )

    class Meta(object):
        verbose_name = "subject"
        verbose_name_plural = "subjects"
        ordering = ['language', 'title']

    @property
    def states(self):
        states = []

        for state in self.STATE_CHOICES:
            states.append(state)

        return states

    def __unicode__(self):
        return u'%s' % (self.title)


def check_url():
    url_report = {}

    subjects = Subject.objects.all()

    for subject in subjects:
        if subject.url:
            try:
                url_status = urllib2.urlopen(subject.url, timeout=3).getcode()
            except Exception, e:
                url_status = "The following error occured: %s" % e
        else:
          url_status = "No URL Found"


        url_report[subject.title] = {'url_status': url_status}

    return url_report


class SubjectBulkUpload(CreatedModifiedMixin, models.Model):
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
    user = models.ForeignKey(User, related_name="subject_bulk_uploads",
                             null=True, blank=True, on_delete=models.SET_NULL)
    xlsx_file = models.FileField(upload_to='subject_bulk_uploads')

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
            record = result['subject']

            try:
                existing_subject = Subject.objects.get(title=record.title, university=record.university,
                                                       code=record.code, language=record.language)
            except Subject.DoesNotExist:
                existing_subject = None
            except Subject.MultipleObjectsReturned:
                existing_subject = Subject.objects.filter(title=record.title,
                                                          university=record.university,
                                                          code=record.code,
                                                          language=record.language)
                existing_subject = existing_subject[0]

            if existing_subject:
                record.pk = existing_subject.pk
                record.created = existing_subject.created

            if record:
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
        from .forms import SubjectFormForBulkUpload

        from ulpa.languages.models import Language
        from ulpa.universities.models import University

        if hasattr(self, '_cached_results'):
            return self._cached_results

        results = []

        xlsx_size = self.xlsx_file._get_size()

        if xlsx_size > self.MAX_UPLOAD_SIZE:
            return results

        xlsx_workbook = load_workbook(self.xlsx_file.file)
        xlsx_sheet = xlsx_workbook.get_active_sheet()

        all_languages = Language.objects.all()
        all_languages_list = list(all_languages)
        all_universities = University.objects.all()
        all_universities_list = list(all_universities)

        for index, row in enumerate(xlsx_sheet.rows):
            if index == 0:
                continue

            errors = []

            try:
                subject_title = row[0].value.strip()
                subject_code = row[1].value
                subject_url = row[2].value
                university_name = row[3].value.strip()
                subject_state = row[4].value.strip()
                other_universities = row[5].value
                subject_intensity = row[6].value.strip()
                language_name = row[7].value.strip()
                prerequisite_languages = row[8].value
                non_beginner_level_available = row[9].value
                subject_next_offered = row[10].value
                subject_study_choice = row[11].value.strip()
                subject_notes = row[12].value
            except AttributeError:
                errors.append('Empty row found, please remove and try again')
                continue
            except IndexError:
                errors.append('Too many rows found, please check your data and try again')
                continue

            try:
                language = [language for language in all_languages_list
                            if language.name == language_name]

                if len(language) >= 1:
                    language = language[0]
                else:
                    language = language

            except Language.DoesNotExist:
                language = None
                errors.append("Invalid language")
            except IndexError:
                errors.append("Language not found")

            try:
                university = [university for university in all_universities_list
                              if university.name == university_name]
                university = university[0]
            except University.DoesNotExist:
                university = None
                errors.append("Invalid university")

            raw_data = {
                'language': language_name,
                'university': university_name,
                'state': subject_state,
                'code': subject_code,
                'title': subject_title,
                'next_offered': subject_next_offered,
                'intensity': subject_intensity,
                'study_choice': subject_study_choice,
                'prerequisite': prerequisite_languages,
                'non_beginner_level_available': non_beginner_level_available,
                'other_university': other_universities,
                'url': subject_url,
                'notes': subject_notes,
            }

            form_language = language_name
            form_university = university_name

            if language:
                form_language = language.pk

            if university:
                form_university = university.pk

            if non_beginner_level_available:
                non_beginner_level_available = True
            elif non_beginner_level_available:
                non_beginner_level_available = False


            if subject_intensity.lower() == Subject.INTENSIVE_TEXT.lower():
                subject_intensity = Subject.INTENSIVE_TEXT
            elif subject_intensity.lower() == Subject.REGULAR_TEXT.lower():
                subject_intensity = Subject.REGULAR_TEXT
            elif subject_intensity.lower() == Subject.REGULAR_AND_INTENSIVE.lower():
                subject_intensity = Subject.REGULAR_TEXT + ',' + Subject.INTENSIVE_TEXT
            elif subject_intensity.lower() == Subject.BOTH.lower():
                subject_intensity = Subject.REGULAR_TEXT + ',' + Subject.INTENSIVE_TEXT

            if subject_study_choice.lower() == Subject.YES.lower() or subject_study_choice.lower() == Subject.ONLINE.lower() or subject_study_choice.lower() == Subject.ALTONLINE.lower():
                subject_study_choice = Subject.ONLINE
            elif subject_study_choice.lower() == Subject.NO.lower() or subject_study_choice.lower() == Subject.FACE_TO_FACE.lower():
                subject_study_choice = Subject.FACE_TO_FACE
            elif subject_study_choice.lower() == Subject.BOTH.lower():
                subject_study_choice = Subject.FACE_TO_FACE + ',' + Subject.ONLINE

            form_data = {
                'language': form_language,
                'university': form_university,
                'state': subject_state,
                'code': subject_code,
                'title': subject_title,
                'next_offered': subject_next_offered,
                'intensity': subject_intensity,
                'study_choice': subject_study_choice,
                'prerequisite': prerequisite_languages,
                'non_beginner_level_available': non_beginner_level_available,
                'other_university': other_universities,
                'url': subject_url,
                'notes': subject_notes,
            }

            form = SubjectFormForBulkUpload(form_data)

            if form.is_valid():
                pass
            else:
                for field, field_errors in form.errors.iteritems():
                    for error in field_errors:
                        message = u'%s - %s' % (SubjectFormForBulkUpload.FIELD_NAMES[field], error)
                        errors.append(message)

            if not errors:
                subject = form.save(commit=False)
            else:
                subject = None

            result = {
                'raw_data': raw_data,
                'form_data': form_data,
                'subject': subject,
                'errors': errors,
            }

            results.append(result)

        self._cached_results = results

        return results
