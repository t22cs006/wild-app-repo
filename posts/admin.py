from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'lat',
        'lon',
        'timestamp',
        'created_at',
        'is_valid',
        'source',
        'presence',
        'species',
    )
    list_filter = ('is_valid', 'source', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'image')
        }),
        ('投稿情報', {
            'fields': ('presence', 'species', 'time_mode')
        }),
        ('位置情報', {
            'fields': ('lat', 'lon', 'source')
        }),
        ('時刻情報', {
            'fields': ('timestamp', 'created_at')
        }),
        ('状態', {
            'fields': ('is_valid',),
        }),
    )
