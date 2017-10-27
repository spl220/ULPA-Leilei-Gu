import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from ulpa.universities.models import University
from ulpa.subjects.models import Subject

from .models import Language, LanguageCategory, LanguageBulkUpload
from .forms import LanguageSearchForm, LanguagesBulkUploadForm


@login_required
def languages_bulk_upload(request):
    """
    Initial page for bulk uploading Subjects within a XLSX file.
    If errors occur with file upload, deals with it here (not
    including parsing errors). Then passes the created bulk_upload
    to the confirm view below
    """
    template = "languages/bulk_upload.html"
    if request.method == 'POST':
        form = LanguagesBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bulk_upload = form.save(commit=False)
            bulk_upload.user = request.user

            bulk_upload.save()

            return redirect('languages:languages-confirm-bulk-upload', bulk_upload.pk)
        else:
            messages.error(request, "There was a problem with your submission,\
                                    please check the form below for errors and\
                                    try again")
    else:
        form = LanguagesBulkUploadForm()

    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def languages_confirm_bulk_upload(request, bulk_upload_id):
    """
    Takes the bulk_upload created above and processes the data.
    Deals with errors if they occur, else, lets the user know
    how many subjects were successfully created.
    """

    template = "languages/confirm_bulk_upload.html"

    bulk_upload = get_object_or_404(LanguageBulkUpload, pk=bulk_upload_id)

    if not bulk_upload.is_pending:
        messages.error(request, "Sorry, the bulk upload you were accessing has\
                                 already been actioned. Please re-upload your\
                                 XLSX file.")

    results = bulk_upload.results

    if request.method == "POST":
        if 'submit_confirm' in request.POST and not bulk_upload.errors:
            languages = bulk_upload.process()

            added_languages = languages.get('languages')
            added_categories = languages.get('categories')

            messages.success(request, "%s languages created successfully. %s categories created successfully" % (len(added_languages), len(added_categories)))
            return redirect('core:home')

        elif 'submit_cancel' in request.POST:
            bulk_upload.cancel()
            messages.success(request, "Bulk upload cancelled")
            return redirect('languages-bulk-upload')

    context = {
        'bulk_upload': bulk_upload,
        'results': results,
    }

    return render(request, template, context)


def individual_language(request, *args, **kwargs):

    template = "languages/individual_language.html"

    language = kwargs.get('language')

    individual_language = get_object_or_404(Language, slug__iexact=language)
    subject_universities = Subject.objects.filter(language__slug=language).values_list('university', flat=True).distinct()
    universities_with_language = University.objects.filter(pk__in=subject_universities)

    context = {
        'universities_with_language': universities_with_language,
        'individual_language': individual_language,
    }

    return render(request, template, context)


def category_language(request, *args, **kwargs):

    template = "languages/category_language.html"

    category = kwargs.get('category')

    category_language = get_object_or_404(LanguageCategory, slug__iexact=category)
    individual_languages = Language.objects.filter(categories=category_language)

    context = {
        'category_language': category_language,
        'individual_languages': individual_languages,
    }

    return render(request, template, context)


def language_search(request, *args, **kwargs):

    template = "languages/language_search.html"

    state_choices = Subject.STATE_CHOICES
    states = []
    all_subjects = Subject.objects.all()

    for state in state_choices:
        universities = University.objects.filter(subjects__state=state[0]).distinct()
        states.append((state[0], universities))

    states.sort()
    form = LanguageSearchForm(request.GET or None)

    if form.is_valid():

        form = LanguageSearchForm(request.GET)

    context = {
        'form': form,
        'states': states,
    }

    return render(request, template, context)

def list_potential_subjects(request):
    response_subject = {}
    language_query = []
    all_subjects = Subject.objects.all()
    for var in request.GET:
        languageselected = request.GET.get(var)
        found_subjects = all_subjects.filter(language__name = languageselected)
        response_subject[languageselected] = len(found_subjects)

    return JsonResponse(response_subject, safe=False)


def list_universities(request):
    language_query = []
    response_universities = {}
    all_subjects = Subject.objects.all()
    state_choices = Subject.STATE_CHOICES
    states = []
    response_subjects = {}
    for var in request.GET:
        language = request.GET.get(var)
        language_query.append(language)
      
    available_subjects = Subject.objects.filter(language__name__in=language_query).select_related('university')
    
    for subject in available_subjects:
        if subject.state in response_universities:
            if subject.university.name in response_universities[subject.state]:
                pass
            else:
                response_universities[subject.state] += [subject.university.name]
        else:
            response_universities[subject.state] = [subject.university.name]

    for state in response_universities:
       for university in response_universities[state]:

           found_subjects = all_subjects.filter(language__name__in=language_query, university__name = university)
           if state in response_subjects:
              response_subjects[state] +=[(university,len(found_subjects))]
           else:
              response_subjects[state] = [(university,len(found_subjects))]

    return JsonResponse(response_subjects, safe=False)
