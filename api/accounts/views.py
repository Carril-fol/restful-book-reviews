import jwt

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken

from .serializers import UserRegisterSerializer, UserLoginSerializer
from .utils import generate_tokens

# Create your views here.
class TokenDecoder(APIView):

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
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data=request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.check(data)
            serializer.save()

            return Response({"Message": "User registered"}, status=status.HTTP_200_OK)
        return Response({"Error", serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Example:

    POST: users/api/login/

    ```
    Application data:

    {
        username: "Username from the user"
        password: "Password from the user"
    }

    Successful response (code 200 - OK):
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZW1haWwiOiJmb2xjby5jYXJyaWwyQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJmb2xjbyIsImxhc3RfbmFtZSI6ImNhcnJpbCIsImlzX3N0YWZmIjpmYWxzZSwiaXNfc3VwZXJ1c2VyIjpmYWxzZSwiaXNfdmVyaWZpZWQiOnRydWUsImV4cCI6MTcxMDQ1OTU1NX0.rX-zYs0GlNmuMVmkrUFlvzc2OCL2hqS6a7dPmd7ioU8",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNzEwOTc3OTU1fQ.MSmFM8xm0lM07DHm1rA8-nXmX05J9Zo7Qi98OjVTbYg"
    }

    Response with validation errors (code 400 - Bad Request):
    {
        "username": [This field is obligatory.]
        "password": [This field is obligatory.]
        // Other errors of validation from the serializer.
    }
    ```
    """
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data=request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            user_data = serializer.check_user_exists(data)
            tokens = generate_tokens(user_data)
            response = Response({'access': tokens['access'], 'refresh': tokens['refresh']}, status=status.HTTP_200_OK)
            response.set_cookie('access', tokens["access"])
            response.set_cookie('refresh', tokens["refresh"])
            return response
        response = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
    

class LogoutView(APIView):
    """
    Example:

    POST: users/api/logout/

    ```
    Cookies data:

    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZW1haWwiOiJmb2xjby5jYXJyaWwyQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJmb2xjbyIsImxhc3RfbmFtZSI6ImNhcnJpbCIsImlzX3N0YWZmIjpmYWxzZSwiaXNfc3VwZXJ1c2VyIjpmYWxzZSwiaXNfdmVyaWZpZWQiOnRydWUsImV4cCI6MTcxMDQ1OTU1NX0.rX-zYs0GlNmuMVmkrUFlvzc2OCL2hqS6a7dPmd7ioU8",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNzEwOTc3OTU1fQ.MSmFM8xm0lM07DHm1rA8-nXmX05J9Zo7Qi98OjVTbYg"
    }

    Successful response (code 200 - OK):
    {
        'Message': 'Successful logout'
    }

    Response with validation errors (code 400 - Bad Request):
    {
        'Error': 'Token not found in cookies'
    }
    ```
    """
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        access_token = request.COOKIES.get('access')
        if refresh_token and access_token:
            try:
                token_to_blacklist = RefreshToken(refresh_token).blacklist()
            except InvalidToken as error:
                return Response({'Error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
            
            response = Response({'Message': 'Logout successfully'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh')
            response.delete_cookie('access')
            return response
        response = Response({'Error': 'Token not found in cookies'}, status=status.HTTP_400_BAD_REQUEST)
        return response