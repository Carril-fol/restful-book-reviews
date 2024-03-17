import jwt

from django.conf import settings
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .permissions import isVerified
from .models import UserCustom
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .utils import send_verification_email, TokenView

# Create your views here.
def activate_account(request, token):
    """
    Activates a user account using the provided activation token.
    """
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = decoded_token['user_id']
    try:
        user = UserCustom.objects.get(id=user_id)
    except (jwt.ExpiredSignatureError, jwt.DecodeError, UserCustom  .DoesNotExist):
        return JsonResponse({"Error": "User not found or invalid token."}, status=404)
        
    user.is_verified = True
    user.save()
    return JsonResponse({"Message": "User account activated successfully."}, status=200)


class RegisterView(APIView):
    """
    Example:

    POST: api/register/

    ```
    Application data:

    {
        username: "Username from the user"
        first_name: "First name from the user"
        last_name: "Last name from the user"
        email: "Email from the user"
        password: "Password from the user"
        confirm_password: "Confirm password from the user"
    }

    Successful response (code 201 - Created):
    {
        "Message": "Email verification send"
    }

    Response with validation errors (code 400 - Bad Request):
    {
        "username": ["This field has to be unique"],
        "first_name": ["This field is obligatory."],
        "last_name": ["This field is obligatory."],
        "email": ["This field has to be unique."],
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
            user = serializer.save()
            email_send = send_verification_email(user)
            return Response({"Message": "Email verification send"}, status=status.HTTP_201_CREATED)
        return Response({"Error", serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    """
    Example:

    POST: users/api/login/

    ```
    Application data:

    {
        "email": "Email from the user",
        "password": "Password from the user"
    }

    Successful response (code 200 - OK):
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZW1haWwiOiJmb2xjby5jYXJyaWwyQGdtYWlsLmNvbSIsImZpcnN0X25hbWUiOiJmb2xjbyIsImxhc3RfbmFtZSI6ImNhcnJpbCIsImlzX3N0YWZmIjpmYWxzZSwiaXNfc3VwZXJ1c2VyIjpmYWxzZSwiaXNfdmVyaWZpZWQiOnRydWUsImV4cCI6MTcxMDQ1OTU1NX0.rX-zYs0GlNmuMVmkrUFlvzc2OCL2hqS6a7dPmd7ioU8",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNzEwOTc3OTU1fQ.MSmFM8xm0lM07DHm1rA8-nXmX05J9Zo7Qi98OjVTbYg"
    }

    Response with validation errors (code 400 - Bad Request):
    {
        "email": [This field is obligatory.],
        "password": [This field is obligatory.],
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
            serializer.check(data)
            user_data = serializer.user_data(data)
            tokens = TokenView().generate_tokens(user_data)
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
    permission_classes = [isVerified]

    def post(self, request):
        tokens = TokenView().get(request)
        refresh_token = tokens[1]
        blacklist_token = TokenView().token_blacklist(refresh_token)

        response = Response({'Message': 'Logout successfully'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh')
        response.delete_cookie('access')
        return response