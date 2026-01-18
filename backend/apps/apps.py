from django.apps import AppConfig


class SignalsConfig(AppConfig):
    name = "apps.signals"

    def ready(self):
        from . import billing_signals
        from . import inventory_signals
        from . import operations_signals
        from . import workorder_signals
