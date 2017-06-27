from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Subject, SubjectBulkUpload
from .forms import SubjectsBulkUploadForm, SubjectSearchForm


@login_required
def subjects_bulk_upload(request):
    """
    Initial page for bulk uploading Subjects within a XLSX file.
    If errors occur with file upload, deals with it here (not
    including parsing errors). Then passes the created bulk_upload
    to the confirm view below
    """
    template = "subjects/bulk_upload.html"
    if request.method == 'POST':
        form = SubjectsBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bulk_upload = form.save(commit=False)
            bulk_upload.user = request.user

            bulk_upload.save()

            return redirect('subjects:subjects-confirm-bulk-upload', bulk_upload.pk)
        else:
            messages.error(request, "There was a problem with your submission,\
                                    please check the form below for errors and\
                                    try again")
    else:
        form = SubjectsBulkUploadForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def subjects_confirm_bulk_upload(request, bulk_upload_id):
    """
    Takes the bulk_upload created above and processes the data.
    Deals with errors if they occur, else, lets the user know
    how many subjects were successfully created.
    """

    template = "subjects/confirm_bulk_upload.html"

    bulk_upload = get_object_or_404(SubjectBulkUpload, pk=bulk_upload_id)

    if not bulk_upload.is_pending:
        messages.error(request, "Sorry, the bulk upload you were accessing has\
                                 already been actioned. Please re-upload your\
                                 XLSX file.")

    results = bulk_upload.results

    if request.method == "POST":
        if 'submit_confirm' in request.POST and not bulk_upload.errors:
            subjects = bulk_upload.process()
            messages.success(request, "%s subjects created successfully" % len(subjects))
            return redirect('core:home')

        elif 'submit_cancel' in request.POST:
            bulk_upload.cancel()
            messages.success(request, "Bulk upload cancelled")
            return redirect('subjects:subjects-bulk-upload')

    context = {
        'bulk_upload': bulk_upload,
        'results': results,
    }

    return render(request, template, context)


def subject_search_results(request, *args, **kwargs):

    template = "subjects/search_results.html"
    available_online = "online"
    sort_order = ""
    number_of_pages = []

    search_parameters = request.GET.copy()

    if 'page' in search_parameters:
        del search_parameters['page']
    if 'sort_by' in search_parameters:
        sort_order = request.GET.get('sort_by')
        del search_parameters['sort_by']

    found_subjects = {}

    if len(request.GET):

        languages = request.GET.getlist('language', None)
        universities = request.GET.getlist('university', None)
        study_choices = request.GET.get('study_choice', None)
        intensities = request.GET.get('intensity', None)

        found_subjects = Subject.objects.all()

        if languages:
            found_subjects = found_subjects.filter(language__name__in=languages)
        if universities:
            found_subjects = found_subjects.filter(university__name__in=universities)
        if study_choices:
            found_subjects = found_subjects.filter(
                study_choice__icontains=study_choices
            )
        if intensities:
            found_subjects = found_subjects.filter(
                intensity__icontains=intensities
            )

        if sort_order.lower() == 'language':
            found_subjects = found_subjects.select_related('university', 'language')\
                                           .order_by('language', 'title')
        elif sort_order.lower() == 'university':
            found_subjects = found_subjects.select_related('university', 'language')\
                                           .order_by('university', 'language')

    if request.method == 'GET':

        form = SubjectSearchForm(request.GET)

    else:

        form = SubjectSearchForm()

    if found_subjects:
        paginator = Paginator(found_subjects, 6)
        page = request.GET.get('page')
        try:
            subjects = paginator.page(page)
        except PageNotAnInteger:
            subjects = paginator.page(1)
        except EmptyPage:
            subjects = paginator.page(paginator.num_pages)
    else:
        subjects = None

    if subjects:
        for page in range(subjects.paginator.num_pages):
            number_of_pages.append(page)

    context = {
        'available_online': available_online,
        'search_parameters': search_parameters,
        'subjects': subjects,
        'sort_order': sort_order,
        'form': form,
        'number_of_pages': number_of_pages,
    }

    return render(request, template, context)


def printable_subject_search_results(request, *args, **kwargs):

    template = "subjects/printable_search_results.html"
    available_online = "online"
    sort_order = ""

    search_parameters = request.GET.copy()

    if 'page' in search_parameters:
        del search_parameters['page']
    if 'sort_by' in search_parameters:
        sort_order = request.GET.get('sort_by')
        del search_parameters['sort_by']

    found_subjects = {}

    if len(request.GET):

        languages = request.GET.getlist('language', None)
        universities = request.GET.getlist('university', None)
        study_choices = request.GET.get('study_choice', None)
        intensities = request.GET.get('intensity', None)

        found_subjects = Subject.objects.all()

        if languages:
            found_subjects = found_subjects.filter(language__name__in=languages)
        if universities:
            found_subjects = found_subjects.filter(university__name__in=universities)
        if study_choices:
            found_subjects = found_subjects.filter(
                study_choice__icontains=study_choices
            )
        if intensities:
            found_subjects = found_subjects.filter(
                intensity__icontains=intensities
            )

        if sort_order.lower() == 'language':
            found_subjects = found_subjects.select_related('university', 'language')\
                                           .order_by('language', 'title')
        elif sort_order.lower() == 'university':
            found_subjects = found_subjects.select_related('university', 'language')\
                                           .order_by('university', 'title')

        if sort_order.lower() == 'language':
            found_subjects = found_subjects.select_related('university', 'language')\
                                           .order_by('language', 'title')
        elif sort_order.lower() == 'university':
            found_subjects = found_subjects.select_related('university', 'language')\
                                           .order_by('university', 'title')

    if request.method == 'GET':

        form = SubjectSearchForm(request.GET)

    else:

        form = SubjectSearchForm()


    context = {
        'available_online': available_online,
        'search_parameters': search_parameters,
        'subjects': found_subjects,
        'sort_order': sort_order,
        'form': form,
    }

    return render(request, template, context)
