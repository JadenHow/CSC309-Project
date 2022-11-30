from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# TODO: User model needs to be updated to have a subscribed bool field and a reference to their subscription plan (default null)
class RegisterUser(models.Model):
    class Meta:
        verbose_name = 'Register User'
        verbose_name_plural = 'Register Users'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=120, blank=False, null=False)
    password = models.CharField(max_length=120, blank=False, null=False)
    email = models.CharField(max_length=120, blank=True, null=True)
    first_name = models.CharField(max_length=120, blank=True, null=True)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True)
    phone_number = models.CharField(max_length=120, blank=True, null=True)
    credit_card_number = models.CharField(max_length=16, blank=True, null=True)
    subscribed = models.BooleanField(default=False)


class Enrolled(models.Model):
    class Meta:
        verbose_name = 'Enrolled User'
        verbose_name_plural = 'Enrolled Users'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_instance = models.ForeignKey('classes.ClassInstances', on_delete=models.CASCADE)


class PaymentHistory(models.Model):
    class Meta:
        verbose_name = 'Payment History'
        verbose_name_plural = 'Payment Histories'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(blank=False, null=False) #enforce positive?
    card_info = models.CharField(max_length=16, blank=True, null=True)
    date = models.DateTimeField(blank=False, null=False)