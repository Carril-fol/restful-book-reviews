import jwt

from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

def decode_token(self, token):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        return user_id
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
def generate_tokens(user):
    refresh_token = RefreshToken.for_user(user)
    access_token = AccessToken.for_user(user)
    tokens = {
        'access': str(access_token),
        'refresh': str(refresh_token)
    }
    return tokens