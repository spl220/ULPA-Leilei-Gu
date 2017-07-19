import collections
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

from ulpa.subjects.models import Subject
from .models import University, UniversityBulkUpload
from .forms import UniversitySearchForm, UniversityBulkUploadForm


def university_search(request):
    template = "universities/university_search.html"

    state_choices = Subject.STATE_CHOICES
    states = []

    for state in state_choices:
        universities = University.objects.filter(subjects__state=state[0]).distinct()
        states.append((state[0], universities))
    states.sort()
    form = UniversitySearchForm(request.GET or None)
    if form.is_valid():
        form = UniversitySearchForm(request.GET)

        # return redirect('subjects:subject-search-results')

    context = {
        'form': form,
        'states': states,
    }

    return render(request, template, context)


def list_languages(request):
    university_query = []
    response_languages = []

    for var in request.GET:
        university = request.GET.get(var)
        university_query.append(university)

    available_subjects = Subject.objects.filter(university__name__in=university_query).select_related('language')

    for subject in available_subjects:
        if subject.language.name in response_languages:
            pass
        else:
            response_languages += [subject.language.name]

    return JsonResponse(response_languages, safe=False)


@login_required
def universities_bulk_upload(request):
    """
    Initial page for bulk uploading universities within a XLSX file.
    If errors occur with file upload, deals with it here (not
    including parsing errors). Then passes the created bulk_upload
    to the confirm view below
    """
    template = "universities/bulk_upload.html"
    if request.method == 'POST':
        form = UniversityBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bulk_upload = form.save(commit=False)
            bulk_upload.user = request.user

            bulk_upload.save()

            return redirect('universities:universities-confirm-bulk-upload', bulk_upload.pk)
        else:
            messages.error(request, "There was a problem with your submission,\
                                    please check the form below for errors and\
                                    try again")
    else:
        form = UniversityBulkUploadForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def universities_confirm_bulk_upload(request, bulk_upload_id):
    """
    Takes the bulk_upload created above and processes the data.
    Deals with errors if they occur, else, lets the user know
    how many universities were successfully created.
    """

    template = "universities/confirm_bulk_upload.html"

    bulk_upload = get_object_or_404(UniversityBulkUpload, pk=bulk_upload_id)

    if not bulk_upload.is_pending:
        messages.error(request, "Sorry, the bulk upload you were accessing has\
                                 already been actioned. Please re-upload your\
                                 XLSX file.")

    results = bulk_upload.results

    if request.method == "POST":
        if 'submit_confirm' in request.POST and not bulk_upload.errors:
            universities = bulk_upload.process()
            messages.success(request, "%s universities created successfully" % len(universities))
            return redirect('core:home')

        elif 'submit_cancel' in request.POST:
            bulk_upload.cancel()
            messages.success(request, "Bulk upload cancelled")
            return redirect('universities:universities-bulk-upload')

    context = {
        'bulk_upload': bulk_upload,
        'results': results,
    }

    return render(request, template, context)
