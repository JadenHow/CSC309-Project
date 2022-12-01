from django.contrib import admin
from .models import Account, PaymentMethod, Purchase
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
class AccountInline(admin.StackedInline):
    model = Account
    #fields = ['first_name', 'last_name', 'email', 'avatar']
    verbose_name_plural = 'account'
    
class UserAdmin(BaseUserAdmin):
    #fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'subscription', 'phone_number']
    #readonly_fields = ['id']
    #list_display = ['id', 'first_name', 'last_name', 'email', 'avatar', 'subscription', 'phone_number']
    inlines = [AccountInline]

class PurchaseInline(admin.StackedInline):
    model = Purchase
    fields = ['user', 'price', 'date', 'purchase_name']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Purchase)