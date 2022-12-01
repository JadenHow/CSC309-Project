from rest_framework import serializers, viewsets
from django.contrib.auth.models import User

from .models import Account, PaymentMethod, Purchase
from subscriptions.serializers import SubscriptionSerializer
from phonenumber_field.serializerfields import PhoneNumberField

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "cc_number", "cc_expiry", "cc_code"]
        
    def create(self, validated_data):
        # payment_method = PaymentMethod.objects.create(cc_number=validated_data['cc_number'],
        #                                               cc_expiry=validated_data['cc_expiry'],
        #                                               cc_code=validated_data['cc_code'])
        payment_method = PaymentMethod.objects.create(**validated_data)
        # update current users payment method
        user = self.context.get('request').user
        user.account.payment_method = payment_method
        user.save()
        # update all future payments to this new card
        future_purchases = Purchase.objects.filter(user=user.account, upcoming=True)
        for p in future_purchases:
            p.card = payment_method
        return payment_method

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        extra_kwargs = {'password': {'required': True, 'write_only': True},
                        'username': {'required': True},
                        'first_name': {'required': True}, 
                        'last_name': {'required': True},
                        'email': {'required': True}}

class RegisterAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    avatar = serializers.ImageField(required=False)
    phone_number = PhoneNumberField(region='CA', required=False)
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": "Email already exists"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('email'), email=validated_data.get('email'), first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'), password=validated_data.get('password'))
        user.account.phone_number = validated_data.get('phone_number')
        user.account.avatar = validated_data.get('avatar')
        user.save()
        return user.account

    def update(self, instance, validated_data):
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.username = validated_data.get('email', instance.user.username)
        instance.user.first_name = validated_data.get('first_name', instance.user.first_name)
        instance.user.last_name = validated_data.get('last_name', instance.user.last_name)
        if (validated_data.get('password')):
            instance.user.set_password(validated_data.get('password'))
        instance.user.save()
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance

class AccountSerializer(serializers.ModelSerializer):
    payment_method = PaymentSerializer(required=False)
    subscription = SubscriptionSerializer(required=False)
    user = UserSerializer(required=False)
    
    class Meta:
        model = Account
        fields = ["id", "user", "phone_number", "avatar", "payment_method", "subscription"]
        #fields = ["id", "username", "email", "first_name","last_name", "phone_number", "avatar", "payment_method", "subscription"]
        # extra_kwargs = {'password': {'required': True, 'write_only': True},
        #                 'first_name': {'required': True}, 
        #                 'last_name': {'required': True}}
    
    avatar = serializers.SerializerMethodField() #user.account.avatar
    def get_avatar(self, obj):
        if not obj.avatar:
            return None
        img = obj.avatar
        #return img
        request = self.context.get('request')
        return request.build_absolute_uri(img.image.url)
    
    phone_number = serializers.SerializerMethodField()
    def get_phone_number(self, obj):
        return obj.phone_number.as_e164

# class  AccountLoginSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = User
#         fields = ["id", "email", "password"]
    
class PurchaseSerializer(serializers.ModelSerializer):
    user = AccountSerializer(read_only=True)
    card = PaymentSerializer(read_only=True)
    
    class Meta:
        model = Purchase
        fields = ('id', 'purchase_name', 'date', 'price', 'upcoming', 'user', 'card')