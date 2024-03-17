from rest_framework.permissions import BasePermission

from accounts.models import UserCustom
from accounts.utils import tokens_in_cookies, TokenView

from .models import Review

class hisReview(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        tokens = TokenView().get(request)
        tokens_valid_status = TokenView().valid_tokens(tokens)
        tokens_in_cookies_valid = tokens_in_cookies(tokens_valid_status)
        if tokens_in_cookies_valid == True:
            refresh_token = tokens[1]
            user_id_decoded = TokenView().decode_token(refresh_token)
            user_data = UserCustom.objects.get(id=user_id_decoded)
            review_data = Review.objects.get(user_creator=user_data.pk)
            if review_data.profile_creator.user.pk == user_data.pk:
                return super().has_object_permission(request, view, obj)
            return False
        