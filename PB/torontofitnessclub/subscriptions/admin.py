from django.contrib import admin
from .models import Subscription

# Register your models here.

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fields = ['name', 'price', 'payment_interval']

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'price', 'payment_interval']
    readonly_fields = ['id']
    list_display = ['name', 'price', 'payment_interval']
    #inlines = [SubscriptionInline]

admin.site.register(Subscription, SubscriptionAdmin)