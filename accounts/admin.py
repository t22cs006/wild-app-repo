from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "present_count", "absent_count", "rare_found")
    search_fields = ("user__username",)
