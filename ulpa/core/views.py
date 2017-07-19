from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from ulpa.core.forms import LanguageSearchForm, ContactForm, URLCheckForm
from ulpa.core.emails import contact_form_sent_handler
from ulpa.languages.models import Language, LanguageCategory
from ulpa.subjects.models import check_url as check_subject_urls
from ulpa.universities.models import University, check_url as check_university_urls
from ulpa.users.models import User

def setup(request):
    """
    Performs initial site setup
    """
    existing_admin_users = User.objects.filter(is_superuser=True)

    if not existing_admin_users:
        user = User(username='admin', email='evan.brumley@wspdigital.com')

        user.set_password('123')
        
        user.is_superuser = True
        user.is_staff = True
        
        user.save()
    else:
        user = None

    context = {
        'user': user,
    }

    return redirect('core:home')


def force_500(request):
    """
    For testing exception handling
    """
    if request.user.is_superuser:
        raise Exception("Test Exception")
    else:
        return redirect('core:home')


def google_verification(request):
    """
    For Googe Seach Console integration
    """
    template = "google_verification.html"

    context = {
    }

    if request.user.is_superuser:
        return render(request, template, context)
    else:
        return redirect('core:home')


def home(request):

    template = "core/home.html"

    context = {
    }

    return render(request, template, context)


def about(request):

    template = "core/about.html"

    context = {
    }

    return render(request, template, context)


def contact(request):

    template = "core/contact.html"

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_form_sent_handler(form)
            messages.success(request, "Message sent successfully")
            return redirect('core:home')
            # except Exception, e:
            #     messages.error(request, "An error occured and the message has not sent successfully. Please try again later. %s" % e)

    context = {
        'form': form,
    }

    return render(request, template, context)


def faq(request):

    template = "core/faq.html"

    context = {
    }

    return render(request, template, context)


def what_languages_can_i_study(request):

    template = "core/what_languages_can_i_study.html"

    languages = Language.objects.all()
    language_categories = LanguageCategory.objects.all().order_by('name')

    if request.method == 'POST':

        form = LanguageSearchForm(request.POST)

        if form.is_valid():
            language = form.cleaned_data.get('language')

    else:

        form = LanguageSearchForm()

    context = {
        'languages': languages,
        'language_categories': language_categories,
        'form': form,
    }

    return render(request, template, context)


def why_study_languages(request):

    template = "core/why_study_languages.html"

    languages = Language.objects.all()

    context = {
        'languages': languages,
    }

    return render(request, template, context)


def can_study_at_uni_other_than_own(request):

    template = "core/can_study_at_uni_other_than_own.html"

    # TODO - Needs updating to appropriate content!

    universities = University.objects.all()

    context = {
        'universities': universities,
    }

    return render(request, template, context)


def where_can_study_indigenous_languages(request):
    INDIGENOUS_LANGUAGES_SLUG = 'Australian Indigenous Languages'
    template = "core/where_can_study_indigenous_languages.html"

    universities = University.objects.all()
    indigenous_languages = Language.objects.filter(categories__name=INDIGENOUS_LANGUAGES_SLUG)

    context = {
        'indigenous_languages': indigenous_languages,
    }

    return render(request, template, context)


def health_check(request):
    template = "health_check.xml"

    status = 200

    context = {
        'status': "OK",
        'response_time': 1.1,  # TODO: Figure out wtf is going here
    }

    return render(request, template, context, status=status, content_type="text/xml")

@login_required
def url_check(request):
    template = "url_check.html"
    university_urls = ""
    subject_urls = ""
    results = {}

    if request.method == 'GET':
        form = URLCheckForm()
    else:
        university_urls = check_university_urls()
        subject_urls = check_subject_urls()
        form = URLCheckForm()

    if university_urls:
        results = {
            'universities': university_urls,
            'subjects': subject_urls,
        }

    context = {
        'form': form,
        'results': results,
    }

    return render(request, template, context)

@login_required
def url_check_results(request):
    template = "url_check_results.html"

    context = {

    }

    return render(request, template, context)


def sitemap(request):
    template = "sitemap.xml"

    context = {

    }

    return render(request, template, context)