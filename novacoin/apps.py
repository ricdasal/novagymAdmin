from django.apps import AppConfig


class NovacoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'novacoin'

    def ready(self):
        import novacoin.signals
