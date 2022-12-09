from django.urls import path
from . import views
from subscriptions.views import SubscribeUserApiView, UpdateUserSubscriptionPlanView, ViewSubscriptionPlansView

app_name = 'subscriptions'
urlpatterns = [
    # path('create/', CreateSubscriptionApiView.as_view()),
    path('<int:subscription_id>/subscribe/', SubscribeUserApiView.as_view()),
    path('edit/', UpdateUserSubscriptionPlanView.as_view()),
    path('', ViewSubscriptionPlansView.as_view())
    # path('renew/', renew_subscriptions_test) # DELETE LATER FOR TESTING ONLY
]