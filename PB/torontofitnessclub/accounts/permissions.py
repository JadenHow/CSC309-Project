from rest_framework.permissions import BasePermission
from .models import Account

class IsSubscribed(BasePermission):
    message = "User does not have an active subscription."
    def has_permission(self, request, view):
        try:
            account = Account.objects.get(user=request.user)
            return request.user.is_authenticated and account.subscription is not None
        except Account.DoesNotExist:
            return False