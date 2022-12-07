from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterUserSerializer, RegisterStaffSerializer
from rest_framework.views import APIView
from rest_framework import permissions, generics
from .models import Enrolled, PaymentHistory, RegisterUser
from .serializers import EnrolledSerializer, RegisterUserSerializer, RegisterStaffSerializer
from classes.models import ClassInstances
from classes.serializers import ClassInstancesSerializer
from subscriptions.models import Subscription, SubscriptionInstance
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from knox.auth import AuthToken, TokenAuthentication
from rest_framework import permissions, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

def serialize_user(user):
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response({
            "user_info": serialize_user(user)
        })

@api_view(['POST'])
def register_staff(request):
    serializer = RegisterStaffSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        return Response({
            "user_info": serialize_user(user)
        })

@api_view(['POST'])
def login(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)
    return Response({
        'user_data': serialize_user(user),
        'token': token
    })

class UserUpdateAPIView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user.username
        curr_user = get_object_or_404(User, username=user)
        curr_register_user = get_object_or_404(RegisterUser, username=user)
        if request.data.get("username"):
            update_username = request.data.get("username")
            if User.objects.all().filter(username=update_username).exists():
                return Response({"msg" : "A user with that Username already exists."}, status=409)
            else:
                curr_user.username = request.data.get("username")
                curr_register_user.username = request.data.get("username")
        if request.data.get("password"):
                curr_user.set_password(request.data.get("password"))
        if request.data.get("email"):
            update_email = request.data.get("email")
            if User.objects.all().filter(email=update_email).exists():
                return Response({"msg" : "A user with that Email already exists."}, status=409)
            else:
                curr_user.email = request.data.get("email")
                curr_register_user.email = request.data.get("email")
        if request.data.get("first_name"):
            curr_user.first_name = request.data.get("first_name")
            curr_register_user.first_name = request.data.get("first_name")
        if request.data.get("last_name"):
            curr_user.last_name = request.data.get("last_name")
            curr_register_user.last_name = request.data.get("last_name")
        if request.data.get("avatar"):
            curr_register_user.avatar = request.data.get("avatar")
        if request.data.get("phone_number"):
            curr_register_user.phone_number = request.data.get("phone_number")
        if request.data.get("credit_card_number"):
            curr_register_user.credit_card_number = request.data.get("credit_card_number")
        
        curr_user.save()
        curr_register_user.save()

        return Response({"msg" : "Successfully edited"}, status=200)

class UserEnrolledListAPIView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = ClassInstancesSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = ''

    def get(self, request):
        user = request.user
        queryset = Enrolled.objects.all().filter(user=user.id)
        data = EnrolledSerializer(queryset, many=True).data

        ls = []
        for obj in data:
            class_instane_id = obj["class_instance"]
            class_instance_obj = ClassInstances.objects.get(pk=class_instane_id)
            instance_data = {
                        'pk': class_instane_id,
                        'studio': class_instance_obj.studio.name,
                        'name': class_instance_obj.name,
                        'description': class_instance_obj.description,
                        'coach': class_instance_obj.coach,
                        'keywords': class_instance_obj.keywords,
                        'capacity': class_instance_obj.capacity,
                        'class_date': class_instance_obj.class_date,
                        'start_time': class_instance_obj.start_time,
                        'end_time': class_instance_obj.end_time,
                    }
            ls.append(instance_data)

        ls.sort(key=lambda x: (x.get('class_date'), x.get('start_time')))
        
        page = self.paginate_queryset(ls)
        return self.get_paginated_response(page)


class GetUserPaymentHistoryApiView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    queryset = ''

    def get(self, request):
        
        queryset = PaymentHistory.objects.filter(user=request.user.id).order_by("date")
        data = list(queryset.values())

        print(data)
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)


class GetUserNextPaymentApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):

        curr_subscription = None
        curr_subscription_instance = None 

        if SubscriptionInstance.objects.filter(user=request.user.id).exists():
            curr_subscription_instance = SubscriptionInstance.objects.get(user=request.user.id)
            curr_subscription = Subscription.objects.get(pk=curr_subscription_instance.parent_subscription.pk)
        else:
            return Response({"msg" : "No subscription currrently active"})

        response_data = {
            "next payment due": curr_subscription_instance.renewal_date,
            "amount due": curr_subscription.price,
            "cancelled": curr_subscription_instance.cancelled
        }

        return Response(response_data, status=200)

# class EnrolledClassAPIView(generics.ListAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Enrolled.objects.all().filter(user=user)
#         data = EnrolledSerializer(queryset, many=True).data
#         return Response(data)

# enrolled_class_view = EnrolledClassAPIView.as_view()
