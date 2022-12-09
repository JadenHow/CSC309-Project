from .models import RegisterUser, Enrolled
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers, validators
from .models import RegisterUser, Enrolled, PaymentHistory
from rest_framework.parsers import MultiPartParser, FormParser

class RegisterUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    parser_classes = (MultiPartParser, FormParser)
    class Meta:
        model = RegisterUser
        fields = [
            "username", 
            "password", 
            "email", 
            "first_name", 
            "last_name",
            "phone_number",
            "avatar",
            "credit_card_number"
            ]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Username already exists."
                    )
                ],
            },
            "email": {
                "required": False,
                "allow_blank": True,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
        }
    
    def create(self, validated_data):
        try:
            validated_data["email"]
            email = validated_data["email"]
        except:
            email = ""
        
        try:
            validated_data["first_name"]
            first_name = validated_data["first_name"]
        except:
            first_name = ""
        
        try: 
            validated_data["last_name"]
            last_name = validated_data["last_name"]
        except:
            last_name = ""
        
        try: 
            validated_data["phone_number"]
            phone_number = validated_data["phone_number"]
        except:
            phone_number = ""
        
        try: 
            validated_data["avatar"]
            avatar = validated_data["avatar"]
        except:
            avatar = ""

        try: 
            print(validated_data["credit_card_number"])
            credit_card_number = validated_data["credit_card_number"]
        except:
            credit_card_number = ""
        
        
        hashed_pwd = make_password(validated_data["password"])
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        RegisterUser.objects.create(
            user=user,
            username=validated_data["username"],
            password=hashed_pwd,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            avatar=avatar,
            credit_card_number=credit_card_number
        )
        return user

class RegisterStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username", 
            "password", 
            "email", 
            "first_name", 
            "last_name",
            ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"A user with that Email already exists."
                    )
                ],
            },
            "first_name": {
                "required": True,
                "allow_blank": False,
            },
            "last_name": {
                "required": True,
                "allow_blank": False,
            },
        }

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user

class EnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrolled
        fields = [
            "user", 
            "class_instance", 
            ]


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = [
            "user",
            "amount",
            "card_info",
            "date"
        ]
