from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import Account, Purchase
from .models import Subscription #, Purchase
from .serializers import SubscriptionSerializer
from accounts.serializers import AccountSerializer, PaymentSerializer, PurchaseSerializer
import datetime
from django.utils import timezone
# from dateutil.relativedelta import relativedelta

from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


# Create your views here.

def cancel_subscription(user, subscription):
    if (not user.subscription or user.subscription.id == subscription.id):
        # delete all future scheduled purchases from this subscription
        user.subscription = None
        user.save()
        cancel_purchases =Purchase.objects.filter(user=user, purchase_name=subscription.name, upcoming=True)
        for p in cancel_purchases:
            p.delete()
    else:
        return False
        #return Response({'error': 'User is not subscribed to ' + subscription.name}, status=400)
    return True
    #return Response({'success': 'User unsubscribed from ' + subscription.name}, status=200)

class UserSubscribeView(APIView):
    """
    User subscribes to subscription {id}
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subscribe_id = self.kwargs.get('pk')
        # serializer = SubscriptionSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        user = request.user
        user = user.account
        sub_ = Subscription.objects.get(id=subscribe_id)
        #sub_.subscribed.add(user)
        if not user.payment_method:
            return Response({'error': 'User has no payment method'}, status=400)
        if user.subscription: # if user is already subscribed to someone, unsubscribe
            cancel_subscription(user, user.subscription)
        user.subscription = sub_
        user.save()
        # pay one subscription now, and set an upcoming payment in the next subscription interval
        Purchase.objects.create(user=user, purchase_name=sub_.name, price=sub_.price, date=datetime.date.today(), 
                                card=user.payment_method, upcoming=False)
        Purchase.objects.create(user=user, purchase_name=sub_.name, price=sub_.price, 
                                date=datetime.date.today() + sub_.payment_interval, 
                                card=user.payment_method, upcoming=True)
        return Response({'success': 'User subscribed to ' + sub_.name}, status=200)
        
class UserUnsubscribeView(APIView):
    """
    User unsubscribes from subscription {id}
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        subscribe_id = self.kwargs.get('pk')
        # serializer = SubscriptionSerializer(data=request.data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=400)
        sub_ = Subscription.objects.get(id=subscribe_id)
        user = request.user
        user = user.account
        # if not user.payment_method:
        #     return Response({'error': 'User has no payment method'}, status=400)
        if cancel_subscription(user, sub_):
            return Response({'error': 'User is not subscribed to ' + sub_.name}, status=400)
        else:
            return Response({'success': 'User unsubscribed from ' + sub_.name}, status=200)
        
class UserPaymentsView(ListAPIView):
    """
    View all of users current and upcoming payments
    """
    #queryset = Purchase.objects.filter(user=)
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        #print(Purchase.objects.filter(user=self.request.user.account))
        return Purchase.objects.filter(user=self.request.user.account)
    # def get_object(self):
    #     return self.request.user
    
class SubscriptionListView(ListAPIView):
    """
    List all subscriptions
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
