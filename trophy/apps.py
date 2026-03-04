from django.apps import AppConfig


class TrophyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trophy'

    def ready(self):
        import trophy.signals
