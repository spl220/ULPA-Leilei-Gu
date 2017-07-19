from django.shortcuts import render

from .models import FAQCategory


def faqs(request):
    """

    """
    template = "faqs/index.html"

    all_faqs = FAQCategory.objects.all()

    context = {
        'all_faqs': all_faqs,
    }

    return render(request, template, context)
