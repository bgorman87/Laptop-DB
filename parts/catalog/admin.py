from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Laptop)
admin.site.register(Part)


class PartVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'part', 'vote_type', 'created', 'updated')
    list_filter = ('part', 'user', 'vote_type')
    search_fields = ('user', 'part', 'vote_type')

class LapVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'laptop', 'vote_type', 'created')
    list_filter = ('user', 'laptop', 'vote_type')
    search_fields = ('user', 'laptop', 'vote_type')

admin.site.register(PartVote, PartVoteAdmin)
admin.site.register(LaptopVote, LapVoteAdmin)

