from rest_framework.permissions import BasePermission

from .utils import TokenView, tokens_in_cookies
from .models import UserCustom

# Create here your permissions.

class isVerified(BasePermission):
    
    def has_permission(self, request, view):
        tokens = TokenView().get(request)
        tokens_valid_status = TokenView().valid_tokens(tokens)
        tokens_in_cookies_valid = tokens_in_cookies(tokens_valid_status)
        if tokens_in_cookies_valid == True:
            refresh_token = tokens[1]
            user_id_decoded = TokenView().decode_token(refresh_token)
            user_data = UserCustom.objects.get(id=user_id_decoded)
            if user_data.is_verified:
                return super().has_permission(request, view)
        return False


class isAdminCustom(BasePermission):
    
    def has_permission(self, request, view):
        tokens = TokenView().get(request)
        tokens_valid_status = TokenView().valid_tokens(tokens)
        tokens_in_cookies_valid = tokens_in_cookies(tokens_valid_status)
        if tokens_in_cookies_valid == True:
            refresh_token = tokens[1]
            user_id_decoded = TokenView().decode_token(refresh_token)
            user_data = UserCustom.objects.get(id=user_id_decoded)
            if user_data.is_superuser or user_data.is_admin or user_data.is_staff:
                return super().has_permission(request, view)
            return False