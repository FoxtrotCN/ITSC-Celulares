from django.apps import AppConfig


class ItscCelularesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'itsc_celulares'

    def ready(self):
        import itsc_celulares.signals

