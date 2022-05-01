from django.contrib import admin

# Register your models here.
from .models import *

class LaptopAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'series', 'laptop_model', 'score', 'verified', 'created_by', 'created', 'updated')
    list_filter = ('manufacturer', 'series', 'laptop_model', 'score', 'verified', 'created_by')
    search_fields = ('laptop_model', 'manufacturer', 'series', 'created_by')

class PartAdmin(admin.ModelAdmin):
    list_display = ('model', 'part_type', 'score', 'verified', 'created_by', 'created', "updated")
    list_filter = ('model', 'laptop_model', 'part_type', 'score', 'verified', 'created_by')
    search_fields = ('model', 'laptop_model', 'part_type', 'created_by')

class SerialNumberAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'created_by', 'created')
    list_filter = ('serial_number', 'created_by')
    search_fields = ('serial_number', 'created_by')

admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Part, PartAdmin)
admin.site.register(Serial_Number, SerialNumberAdmin)


class PartVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'part', 'vote_type', 'created', 'updated')
    list_filter = ('part', 'user', 'vote_type')
    search_fields = ('user', 'part', 'vote_type')

class LaptopVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'laptop', 'vote_type', 'created')
    list_filter = ('user', 'laptop', 'vote_type')
    search_fields = ('user', 'laptop', 'vote_type')

admin.site.register(PartVote, PartVoteAdmin)
admin.site.register(LaptopVote, LaptopVoteAdmin)

class PartChangeAdmin(admin.ModelAdmin):
    list_display = ('part', 'old_model', 'new_model', 'created_by', 'created', 'updated', 'approved', 'approved_by', 'rejected_by', "rejected_reason")
    list_filter = ('part', 'old_model', 'new_model', 'created_by', 'approved', 'approved_by', 'rejected_by')
    search_fields = ('part', 'old_model', 'new_model', 'created_by', 'approved', 'approved_by', 'rejected_by')

class LaptopChangeAdmin(admin.ModelAdmin):
    list_display = ('laptop', 'old_model', 'new_model', 'created_by', 'created', 'updated', 'approved', 'approved_by', 'rejected_by', "rejected_reason")
    list_filter = ('laptop', 'old_model', 'new_model', 'created_by', 'approved', 'approved_by', 'rejected_by')
    search_fields = ('laptop', 'old_model', 'new_model', 'created_by', 'approved', 'approved_by', 'rejected_by')

admin.site.register(PartModelChange, PartChangeAdmin)
admin.site.register(LaptopModelChange, LaptopChangeAdmin)