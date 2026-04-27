from django.apps import AppConfig

class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        from . import operator
        operator.start() # 👈 장고가 준비되면 스케줄러 시작!