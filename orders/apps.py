from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self) -> None:
        # THREADS IMPLEMENTATION
        # from .processor import Processor
        # Processor().start()
        # return super().ready()

        # CELERY WORKER IMPLEMENTATION
        from .tasks import orders_validation

        orders_validation.delay()
