from django.contrib import admin

from .models import ContactUs

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'message_type', 'created_at', 'updated_at')
    list_filter = ('created_by', 'message_type')
    search_fields = ('created_by', 'message_type')

admin.site.register(ContactUs, ContactUsAdmin)