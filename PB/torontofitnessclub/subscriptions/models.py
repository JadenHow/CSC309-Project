from django.db import models
# from accounts.models import Account, PaymentMethod

# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=255)
    price =  models.DecimalField(max_digits=6, decimal_places=2)
    payment_interval = models.DurationField(help_text='enter in the format: "x days"')
    #subscribed = models.ManyToManyField(Account)
    
    def __str__(self):
        return self.name
    
# class Purchase(models.Model):
#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
#     name = models.CharField(max_length=255) # relates to subscription.name
#     price = models.DecimalField(max_digits=6, decimal_places=2)
#     date = models.DateField()
#     card = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, blank=True, null=True)
#     upcoming = models.BooleanField(default=False) # if its a future sub payment yet or already happened