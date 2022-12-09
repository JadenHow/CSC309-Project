from . import views
from django.urls import path
from knox import views as knox_views
from . import views
from users.views import GetUserPaymentHistoryApiView, GetUserNextPaymentApiView, UserEnrolledListAPIView, GetUserInfoView

app_name = 'users'
urlpatterns = [
    path('register/user/', views.register_user),
    path('register/staff/', views.register_staff),
    path('login/', views.login),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
    path('classes/', UserEnrolledListAPIView.as_view()),
    path('paymenthistory/', GetUserPaymentHistoryApiView.as_view()),
    path('nextpayment/', GetUserNextPaymentApiView.as_view()),
    path('edit/', views.UserUpdateAPIView.as_view()),
    path('info/', GetUserInfoView.as_view())
]
