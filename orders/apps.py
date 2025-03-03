from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self) -> None:
        from .processor import Processor

        Processor().start()

        return super().ready()
