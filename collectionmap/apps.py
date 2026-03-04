# collectionmap/apps.py

from django.apps import AppConfig

class CollectionmapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collectionmap'

    def ready(self):
        import collectionmap.signals
