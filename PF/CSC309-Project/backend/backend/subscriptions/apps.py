from django.apps import AppConfig
import sys


class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptions'

    def ready(self):
        if 'runserver' in sys.argv:
            print("starting subscription scheduler")
            from .subscription_scheduler import subscription_renewer
            subscription_renewer.start()
        return
