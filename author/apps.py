from django.apps import AppConfig


class AuthorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'author'

    def ready(self) -> None:
        import author.signals  # noqa
        return super().ready()
