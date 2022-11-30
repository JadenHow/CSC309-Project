from django.db import models
from django.core.exceptions import ValidationError
from users.models import User

# Create your models here.

def validate_occurance(value):
    if value in set("weekly, bi-weekly", "monthly", "annually"):
        return value
    else:
        raise ValidationError("Not a valid occurance")


class Subscription(models.Model):
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        
    price = models.FloatField(blank=False, null=False)
    occurance = models.CharField(max_length=120, blank=False,
                                 null=False,
                                 choices=(
                                    ("weekly", "Weekly"),
                                    ("bi-weekly", "Bi-weekly"),
                                    ("monthly", "Monthly"),
                                    ("annually", "Annually")
                                 ))

# if cancelled is true, then on the payment date we will delete this users subscription instance
class SubscriptionInstance(models.Model):
    class Meta:
        verbose_name = 'Subscription Instance'
        verbose_name_plural = 'Subscription Instances'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE) # A user can only be on one subscription plan at a time
    parent_subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE)
    renewal_date = models.DateField(blank=False, null=False)
    cancelled = models.BooleanField(default=False)

