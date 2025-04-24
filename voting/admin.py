from django.contrib import admin
from .models import VotingCode

class VotingCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used', 'used_at')  # Fields to display in the admin list view

admin.site.register(VotingCode, VotingCodeAdmin)
