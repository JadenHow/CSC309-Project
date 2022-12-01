from django.urls import path
import subscriptions.views as views
urlpatterns = [
    path('', views.SubscriptionListView.as_view(), name='subscription_list'),
    path('payments/', views.UserPaymentsView.as_view(), name='payments_list'),
    path('<int:pk>/subscribe/', views.UserSubscribeView.as_view(), name='subscribe_view'),
    path('<int:pk>/unsubscribe/', views.UserUnsubscribeView.as_view(), name='unsubscribe_view'),
]