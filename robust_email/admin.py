from django.contrib import admin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.conf.urls import patterns, url
from robust_email.models import *


class EmailTransactionInline(admin.TabularInline):
    model = EmailTransaction
    readonly_fields = ('success', 'when', 'exception_type','exception_value',
                       'terminal_error')
    can_delete = False
    extra = 0
    max_num = 0 # no add button


class AttachmentInline(admin.TabularInline):
    model = Attachment
    readonly_fields = ('content', 'mimetype')
    can_delete = False
    extra = 0
    max_num = 0 # no add button


class EmailMessageInline(admin.TabularInline):
    model = EmailMessage
    fields = ('to', 'user', 'subject', 'attempts', 'successful')
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False

    
class EmailMessageAdmin(admin.ModelAdmin):
    inlines=[AttachmentInline, EmailTransactionInline]
    list_display = ('to_address_string', 'subject', 'attempts', 'successful',
                    'cannot_send', 'created')
    readonly_fields = ('to','from_email','bcc','subject','body', 'user')
    search_fields = ('to', 'subject', 'body',)
    date_hierarchy = 'created'

    def resend(self, request, message_id):
        message = get_object_or_404(EmailMessage, pk=message_id)
        status = message.send()
        if status == True:
            messages.success(request, 'The message was resent successfully')
        elif status == False:
            messages.warning(request, 'Message re-sending failed.')
        else:
            messages.info(request, 'Message has been queued for resending')
        return redirect('admin:robust_email_emailmessage_change', message_id)

    def get_urls(self):
        urls = super(EmailMessageAdmin, self).get_urls()
        opts = self.model._meta
        info = opts.app_label, opts.model_name
        my_urls = patterns(
            '',
            url(r'^(\d+)/resend/$',
                self.admin_site.admin_view(self.resend),
                name='%s_%s_resend' % info),
            )
        return my_urls + urls

    
admin.site.register(EmailMessage, EmailMessageAdmin)
