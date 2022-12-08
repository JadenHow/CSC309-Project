from rest_framework import serializers
from .models import Subscription, SubscriptionInstance

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'pk',
            'price',
            'occurance'
        ]

class SubscriptionInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionInstance
        fields = [
            'user',
            'parent_subscription',
            'renewal_date',
            'cancelled',
        ]


class UpdateSubscriptionInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionInstance
        fields = [
            'parent_subscription',
            'cancelled',
        ]