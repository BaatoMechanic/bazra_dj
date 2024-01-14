from django.apps import AppConfig


class VehicleRepairConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vehicle_repair'

    def ready(self) -> None:
        import vehicle_repair.signals
        # return super().ready()
