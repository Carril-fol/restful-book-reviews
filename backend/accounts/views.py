from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.tokens import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

import jwt
from .serializers import AccountSerializer
from profiles.models import Profile

# Create your views here.
class TokenDecoder(APIView):
    authentication_classes = (JWTAuthentication,)

    def decode_token(self, token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
            return user_id
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get(self, request):
        token = request.COOKIES.get('refresh')
        if not token:
            return Response({'Error': 'Token not found in cookies'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user_id = self.decode_token(token)
            if user_id is None:
                return Response({'Error': 'Token not found in cookies'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'user_id': user_id, 'message': 'Decoded token'})


class RegisterView(APIView):
    """
    This feature allows users to register and return a JWT for use in a frontend.

    Example:

    ```
    POST: accounts/api/register/

    Application data:
    {
        "username": "Username from the user",
        "password": "Password from the user",
        "password2": "Confirmation the password",
        "first_name": "First Name from the user",
        "last_name": "Last Name from the user",
        "email": "Email from ther user"
    }

    Successful response (code 201 - Created):
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5hbWUiLCJzdWIiOjEsImV4cCI6MTYzNjU4MTg0MCwianRpIjoiZDYwNzI3YjQ1NzY3NDEyNGFkZjRhOWRlYmZhODRiM2MifQ._bMepZtOkryVCeUZLlGyfgzInqk7KRJgkHau4Mn1o3E",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5hbWUiLCJzdWIiOjEsImV4cCI6MTYzNjU4MTg0MCwianRpIjoiZDYwNzI3YjQ1NzY3NDEyNGFkZjRhOWRlYmZhODRiM2MifQ._bMepZtOkryVCeUZLlGyfgzInqk7KRJgkHau4Mn1o3E"
    }

    Response with validation errors (code 400 - Bad Request):
    {
        "username": ["This field is obligatory."],
        "email": ["This field has to be unique."]
        // Other errors of validation from the serializer.
    }
    ```
    """

    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token_pair_view = TokenObtainPairView.as_view()
            token_request = request._request
            token_request.data = {
                'username': user.username,
                'password': request.data.get('password')
            }
            response = token_pair_view(token_request)
            return Response({'access': response.data['access'], 'refresh': response.data['refresh']}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': serializer.error_messages, 'Error detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({'access': response.data['access'], 'refresh': response.data['refresh']},status=status.HTTP_200_OK)
    

class LogoutView(TokenBlacklistView):
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            token_decoder = TokenDecoder()
            raw_token = request.COOKIES.get('refresh')
            if not raw_token:
                return Response({'error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
            super().post(request)
            return Response({'message': 'Successful logout'},status=status.HTTP_200_OK)
        except TokenError as error_token:
            return Response({'message': 'Invalid refresh token', 'error': str(error_token)},status=status.HTTP_400_BAD_REQUEST)
        

class DeleteAccount(APIView):
    authentication_classes = (JWTAuthentication,)
     
    def delete(self, request):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            get_profile = Profile.objects.get(user=user_id)
            get_user = User.objects.get(id=user_id)
            data_accounts_deleted = {
                'username': get_user.username,
                'email': get_user.email,
                'first_name': get_user.first_name,
                'last_name': get_user.last_name
            }
            if get_profile.user.pk == get_user.pk:
                get_profile.delete()
                get_user.delete()
                return Response({'Message': 'Account and Profile deleted.', 'Account data': data_accounts_deleted}, status=status.HTTP_200_OK)
            return
        except Profile.DoesNotExist:
            return Response({'Message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'Message': 'User not in the database'}, status=status.HTTP_404_NOT_FOUND)