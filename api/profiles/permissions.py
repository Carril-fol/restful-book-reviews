from rest_framework.permissions import BasePermission

from accounts.models import UserCustom
from accounts.utils import tokens_in_cookies, TokenView

from .models import Profile

# Create here your permissions.

class hisProfile(BasePermission):

    def has_permission(self, request, view):
        tokens = TokenView().get(request)
        tokens_valid_status = TokenView().valid_tokens(tokens)
        tokens_in_cookies_valid = tokens_in_cookies(tokens_valid_status)
        if tokens_in_cookies_valid == True:
            refresh_token = tokens[1]
            user_id_decoded = TokenView().decode_token(refresh_token)
            user_data = UserCustom.objects.get(id=user_id_decoded)
            profile_user = Profile.objects.get(user=user_data.pk)
            if profile_user.user.pk == user_data.pk:
                return super().has_permission(request, view)
            return False