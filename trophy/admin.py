from django.contrib import admin
from .models import Trophy, UserTrophy

@admin.register(Trophy)
class TrophyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "condition_type", "condition_value", "rarity")
    search_fields = ("name", "condition_type")
    list_filter = ("rarity", "condition_type")

@admin.register(UserTrophy)
class UserTrophyAdmin(admin.ModelAdmin):
    list_display = ("user", "trophy", "obtained_at")
    list_filter = ("user", "trophy__rarity", "obtained_at")
    search_fields = ("user__username", "trophy__name")
    date_hierarchy = "obtained_at"
