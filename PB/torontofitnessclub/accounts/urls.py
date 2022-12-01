from django.urls import path
from .views import RegisterUserView, AccountPaymentMethod, UpdateAccountView #,LoginAccountView,
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='signup_account'),
    path('edit/', UpdateAccountView.as_view(), name='update_account'),
    path('payment/', AccountPaymentMethod.as_view(), name='update_payment_account'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
#path('login/', LoginAccountView.as_view(), name='login_account'),
#path('logout/', account_logout, name='logout_account'),