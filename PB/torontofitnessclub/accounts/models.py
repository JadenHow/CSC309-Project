from django.db import models
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from phonenumber_field.modelfields import PhoneNumberField
from subscriptions.models import Subscription

from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.
    
class PaymentMethod(models.Model):
    cc_number = CardNumberField('card number')
    cc_expiry = CardExpiryField('expiration date')
    cc_code = SecurityCodeField('security code')
    
    def __str__(self):
        return "Card Number " + self.cc_number
    
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, blank=True, null=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email
    
    @property
    def first_name(self):
        return self.user.first_name
    
    @property
    def last_name(self):
        return self.user.last_name
    
    @receiver(post_save, sender=User)
    def create_user_account(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_account(sender, instance, **kwargs):
        instance.account.save()
    
class Purchase(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_name = models.CharField(max_length=255) # relates to subscription.name
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    card = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
    upcoming = models.BooleanField(default=False) # if its a future sub payment yet or already happened
    
    def __str__(self):
        return str("$"+str(self.price) + " on " + str(self.date) + " for " + self.purchase_name)