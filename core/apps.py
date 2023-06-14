from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Call the ready() method here
        import core.signals  # Import the signals module
        super().ready()  # Call the ready() method of the parent class