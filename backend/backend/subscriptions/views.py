from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics, authentication, permissions
from knox.auth import TokenAuthentication
from .serializers import SubscriptionSerializer, SubscriptionInstanceSerializer, UpdateSubscriptionInstanceSerializer
from rest_framework.response import Response
from .models import Subscription, SubscriptionInstance
from django.shortcuts import get_object_or_404
import datetime
from datetime import timedelta
from users.serializers import PaymentHistorySerializer
from users.models import RegisterUser
from rest_framework.pagination import LimitOffsetPagination
# Create your views here.
class CreateSubscriptionApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        data = {
            'price': request.data.get("price"),
            'occurance': request.data.get("occurance")
        }

        serializer = SubscriptionSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save() 

            return Response({"msg" : "Subscription Created"}, status=200)

        else:
            return Response({"msg" : "Error creating subscription"}, status=404)


class SubscribeUserApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, subscription_id):

        subscription_plan = get_object_or_404(Subscription, pk=subscription_id)
        # print(subscription_plan)
        # print(request.user.id)
        curr_user = get_object_or_404(RegisterUser, user=request.user.id)
        # print(curr_user)

        if SubscriptionInstance.objects.filter(user=request.user.id).exists():
            return Response({"msg" : f"Already subscribed to a plan"}, status=404)
        elif curr_user.credit_card_number == '':
            return Response({"msg" : f"Please enter a credit card for this account"}, status=404)
        

        plan_lengths = {
            "weekly": 7,
            "bi-weekly": 14,
            "monthly": 30,
            "annually": 365
        }

        today = datetime.date.today()

        renewal_date = today + timedelta(days=plan_lengths[subscription_plan.occurance])
        print(renewal_date)

        data = {
            'user': request.user.id,
            'parent_subscription': subscription_id,
            'renewal_date': renewal_date
        }

        serializer = SubscriptionInstanceSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            payment_data = {
                'user': request.user.id,
                'amount': float(subscription_plan.price),
                'card_info': curr_user.credit_card_number,
                'date': datetime.datetime.now(),
            }
            payment_serializer = PaymentHistorySerializer(data=payment_data)

            if payment_serializer.is_valid(raise_exception=True):
                payment_serializer.save()

            serializer.save()
            curr_user.subscribed = True
            curr_user.save()

            return Response({"msg" : f"Successfully subscribed to a {subscription_plan.occurance} renewing plan and will be renewed on {renewal_date}"}, status=200)

        return Response({"msg" : f"Error should never get here"}, status=500)

# @api_view(['POST'])
# def renew_subscriptions_test(request):
#     method = request.method
    
#     if method == 'POST':
#         plan_lengths = {
#                 "weekly": 7,
#                 "bi-weekly": 14,
#                 "monthly": 30,
#                 "annually": 365
#             }

#         queryset = SubscriptionInstance.objects.filter(renewal_date=datetime.date.today())
        
#         for obj in queryset:
#             if obj.cancelled == False:
#                 curr_user = get_object_or_404(RegisterUser, user=obj.user.pk)
#                 curr_subscription = get_object_or_404(Subscription, pk=obj.parent_subscription.pk)

#                 if not curr_user.credit_card_number:
#                     obj.delete()
#                     curr_user.subscribed = False
#                     curr_user.save()
#                     continue

#                 payment_data = {
#                     'user': curr_user.id,
#                     'amount': curr_subscription.price,
#                     'card_info': curr_user.credit_card_number,
#                     'date': datetime.datetime.now(),
#                 }

#                 payment_serializer = PaymentHistorySerializer(data=payment_data)
#                 if payment_serializer.is_valid(raise_exception=True):
#                     payment_serializer.save()

#                 obj.renewal_date = datetime.date.today() + timedelta(days=plan_lengths[curr_subscription.occurance])
#                 curr_user.subscribed = True
#                 curr_user.save()
#                 obj.save()
                
#             else:
#                 curr_user.subscribed = False
#                 curr_user.save()
#                 obj.delete()

#         return Response({"msg" : "Renewals finsihed"}, status=200)

def renew_subscriptions():
    plan_lengths = {
            "weekly": 7,
            "bi-weekly": 14,
            "monthly": 30,
            "annually": 365
        }

    queryset = SubscriptionInstance.objects.filter(renewal_date=datetime.date.today())
    
    for obj in queryset:
        if obj.cancelled == False:
            curr_user = get_object_or_404(RegisterUser, user=obj.user.pk)
            curr_subscription = get_object_or_404(Subscription, pk=obj.parent_subscription.pk)

            if not curr_user.credit_card_number:
                obj.delete()
                curr_user.subscribed = False
                curr_user.save()
                continue

            payment_data = {
                'user': curr_user.id,
                'amount': curr_subscription.price,
                'card_info': curr_user.credit_card_number,
                'date': datetime.datetime.now(),
            }

            payment_serializer = PaymentHistorySerializer(data=payment_data)
            if payment_serializer.is_valid(raise_exception=True):
                payment_serializer.save()

            obj.renewal_date = datetime.date.today() + timedelta(days=plan_lengths[curr_subscription.occurance])
            curr_user.subscribed = True
            curr_user.save()
            obj.save()
            
        else:
            curr_user.subscribed = False
            curr_user.save()
            obj.delete()

    print("Renewals complete")

    # return Response({"msg" : "Renewals finsihed"}, status=200)


class UpdateUserSubscriptionPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):

        curr_subscription = get_object_or_404(SubscriptionInstance, user=request.user.id)

        data = {}
        
        # new_subscription = request.data.get('parent_subscription') 

        if 'parent_subscription' in request.data:
            new_subscription = get_object_or_404(Subscription, pk=request.data.get('parent_subscription'))
            data['parent_subscription'] = new_subscription.pk
        
        if 'cancelled' in request.data:
            if request.data.get('cancelled') == 'True':
                data['cancelled'] = True
            elif request.data.get('cancelled') == 'False':
                data['cancelled'] = False

        if len(data) == 0:
            return Response({"msg" : "No changes were made"}, status=200)


        serializer = UpdateSubscriptionInstanceSerializer(curr_subscription, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg" : "Successfully edited"}, status=200)

        return Response({"msg" : "Should never get here"}, status=404)


class ViewSubscriptionPlansView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = SubscriptionSerializer
    queryset = '' # idk why I need to initalize an empty string queryset here for it to work, I was just copying code from list all classes and that works fine without this 

    def get(self, request):
        queryset = Subscription.objects.all()

        print(queryset)

        data = SubscriptionSerializer(queryset, many=True).data

        print(data)

        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)

        



        



