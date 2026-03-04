from django.contrib import admin
from .models import DangerGrid

@admin.register(DangerGrid)
class DangerGridAdmin(admin.ModelAdmin):
    list_display = ("gx", "gy", "reason", "created_at")
    search_fields = ("gx", "gy", "reason")
