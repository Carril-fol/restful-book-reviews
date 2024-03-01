from datetime import datetime


from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

import jwt
from .serializers import AccountSerializer

# Create your views here.
class TokenDecoder(APIView):
    authentication_classes = [JWTAuthentication]

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
            return Response({'Message': serializer.error_messages, 'Error detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
    This function allows users to log in with their credentials and return JWT tokens for use.

    Example:

    ```
    POST: accounts/api/login/

    Application data:
    {
        "username": "Username from the user",
        "password": "Password from the user",
    }

    Successful response (code 201 - Created):
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5hbWUiLCJzdWIiOjEsImV4cCI6MTYzNjU4MTg0MCwianRpIjoiZDYwNzI3YjQ1NzY3NDEyNGFkZjRhOWRlYmZhODRiM2MifQ._bMepZtOkryVCeUZLlGyfgzInqk7KRJgkHau4Mn1o3E",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5hbWUiLCJzdWIiOjEsImV4cCI6MTYzNjU4MTg0MCwianRpIjoiZDYwNzI3YjQ1NzY3NDEyNGFkZjRhOWRlYmZhODRiM2MifQ._bMepZtOkryVCeUZLlGyfgzInqk7KRJgkHau4Mn1o3E"
    }

    Response with validation errors (code 401 - Unauthorized):
    {
        "detail": "No active account found with the given credentials"
    }
    ```
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response({'access': response.data['access'], 'refresh': response.data['refresh']},status=status.HTTP_200_OK)
    

class LogoutView(APIView):
    """
    This function allows users to logout from their accounts, this is through the deletion of jwt token in cookies.

    ```
    POST: accounts/api/loogut/

    Cookies data:
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5hbWUiLCJzdWIiOjEsImV4cCI6MTYzNjU4MTg0MCwianRpIjoiZDYwNzI3YjQ1NzY3NDEyNGFkZjRhOWRlYmZhODRiM2MifQ._bMepZtOkryVCeUZLlGyfgzInqk7KRJgkHau4Mn1o3E",
    }

    Successful response (code 201 - Created):
    {
        'Message': 'Successful logout'
    }

    Response with validation errors (code 400 - Bad request):
    {
        "Error": "Token is not found in cookies."
    }

    Response with validation errors (code 401 - Unauthorized):
    {
        "Error": "Token invalid"
    }
    ```
    """

    def post(self, request):
        token_decoder = TokenDecoder()
        refresh_token = request.COOKIES.get('refresh')
        if not refresh_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_400_BAD_REQUEST)
        user_id = token_decoder.decode_token(refresh_token)
        if user_id is None:
            return Response({'Error': 'Token invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'No user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        response = Response({'Message': 'Successful logout'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        return response