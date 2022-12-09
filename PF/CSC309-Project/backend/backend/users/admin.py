from django.contrib import admin
from .models import RegisterUser, Enrolled, PaymentHistory

# Register your models here.
admin.site.register(RegisterUser)
admin.site.register(Enrolled)
admin.site.register(PaymentHistory)