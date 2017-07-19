from django.contrib import admin

from .models import (FAQ, FAQCategory)


class FAQAdmin(admin.ModelAdmin):
    model = FAQ

    list_display = ('question', 'created', 'modified')


class FAQCategoryAdmin(admin.ModelAdmin):
    model = FAQCategory

    list_display = ('name', 'created', 'modified')


admin.site.register(FAQ, FAQAdmin)
admin.site.register(FAQCategory, FAQCategoryAdmin)
