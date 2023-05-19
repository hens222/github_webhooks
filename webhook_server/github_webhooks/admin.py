from django.contrib import admin
from .models import PullRequest

@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'state', 'created_at', 'updated_at']
