from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'name', 'price', 'payment_interval')