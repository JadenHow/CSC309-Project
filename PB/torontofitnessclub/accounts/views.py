from django.shortcuts import render
#from .models import Account, PaymentMethod
from .serializers import RegisterAccountSerializer, AccountSerializer, PaymentSerializer #, AccountLoginSerializer,
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#from subscriptions.views import SubscriptionSerializer
#from subscriptions.models import Purchase
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


# Create your views here.

# class RegisterSerializer(serializers.ModelSerializer):
#     payment_method = PaymentSerializer()
    
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'first_name', 'last_name', 
#                   'phone_number', 'password', 'avatar')
#         extra_kwargs = {'password': {'required': True, 'write_only': True},
#                         'first_name': {'requried': True}, 
#                         'last_name': {'requried': True}}

#     avatar = serializers.SerializerMethodField() #user.account.avatar
#     def get_avatar(self, obj):
#         return obj.accounts.avatar
    
#     def create(self, validated_data):
#         user = User.objects.create(validated_data['email'],
#                                    validated_data['first_name'],
#                                    validated_data['last_name'],
#                                    validated_data['phone_number'])
#         #user = User.objects.create(**validated_data)
#         user.set_password(validated_data['password'])
#         user.save()
#         account = Account(user=user)
#         account.avatar = validated_data['avatar']
#         account.save()
#         return account
    
class RegisterUserView(CreateAPIView):
    """
    Creates a new user
    """
    serializer_class = RegisterAccountSerializer
    # permission_classes = (AllowAny,)
    
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=400)
    #     user = serializer.drgtgryhfds
    #     return Response({
    #         'first_name': user.first_name, 
    #         'last_name': user.last_name, 
    #         'email': user.email, 
    #         'phone_number': user.phone_number, 
    #         'avatar': user.account.avatar, 
    #         'payment_method': user.account.payment}, status=200)

# class LoginAccountView(APIView):
#     """
#     Logs in a user
#     """
#     # def get(self, request, *args, **kwargs):
#     #     pass
#     authentication_classes = (TokenAuthentication,)
#     #permission_classes = [IsAuthenticated]
#     serializer_class = AccountLoginSerializer
    
#     def post(self, request):
#         if ('email' not in request.data or 'password' not in request.data):
#             return Response({'msg': 'Credentials missing'}, status=400)
#         # user = authenticate(request, 
#         #                     email=request.POST['email'], 
#         #                     password=request.POST['password'])
#         user = request.user
#         if user is not None:
#             login(request, user)
        
# def account_logout(request):
#     request.user.auth_token.delete()
#     logout(request)
#     return Response(request.user + ' logged out successfully')
    
class UpdateAccountView(RetrieveAPIView, UpdateAPIView):
    """
    Update a users data
    """
    serializer_class = RegisterAccountSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']


    def get_object(self):
        return self.request.user.account
        
# signup, login, logout, edit

class AccountPaymentMethod(CreateAPIView):
    """
    Creates a payment method for a user
    """
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    # def post(self, request):
    #     user = request.user
    #     serializer = PaymentSerializer(data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=400)
    #     user.payment_method = 
        
    
# class UpdateAccounPaymentView(RetrieveAPIView, UpdateAPIView):
#     serializer_class = AccountSerializer
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
        
#     # def get_object(self):
#     #     return self.request.user.account