import jwt

from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken

class TokenView(APIView):

    def decode_token(self, token):
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        return user_id

    def generate_tokens(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        tokens = {
            'access': str(access_token),
            'refresh': str(refresh_token)
        }
        return tokens

    def get(self, request):
        refresh_token = request.COOKIES.get('refresh')
        access_token = request.COOKIES.get('access')
        tokens = [access_token, refresh_token]
        return tokens
    
    @staticmethod
    def valid_tokens(tokens):
        tokens_found = all(token is not None for token in tokens)
        return tokens_found
    
    def token_blacklist(self, token):
        try:
            token_to_blacklist = RefreshToken(token).blacklist()
        except InvalidToken as error:
            return Response({'Error': str(error)}, status=status.HTTP_400_BAD_REQUEST)


def tokens_in_cookies(token_bool):
    if token_bool == None or token_bool == False:
        response = Response({'Error': 'Tokens not found in cookies'}, status=status.HTTP_401_UNAUTHORIZED)
        return response
    return token_bool

def send_verification_email(user):
    token = jwt.encode({'user_id': user.pk}, settings.SECRET_KEY, algorithm='HS256')
    subject = 'E-mail verification'
    message = f'Hello {user.first_name} {user.last_name}\nPlease click on the following link to verify your email: http://127.0.0.1:3000/accounts/activate/{token}/'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])