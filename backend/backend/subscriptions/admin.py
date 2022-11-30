from django.contrib import admin
from .models import Subscription, SubscriptionInstance

# Register your models here.
admin.site.register(Subscription)
admin.site.register(SubscriptionInstance)