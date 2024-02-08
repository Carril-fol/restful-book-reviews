from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import TokenError
from rest_framework.permissions import IsAdminUser

from .serializers import EditorialSerializer
from accounts.views import TokenDecoder

# Create your views here.
class EditorialCreate(APIView):
    authentication_classes = (JWTAuthentication, IsAdminUser,)

    def post(self, request):
        try:
            token_decoder = TokenDecoder()
            raw_token = request.COOKIES.get('refresh')
            if not raw_token:
                return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
            user_id = token_decoder.decode_token(raw_token)
            if user_id is None:
                return Response({'Error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = EditorialSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Message': 'Editorial created in the base.'}, status=status.HTTP_201_CREATED)
        except TokenError as error_token:
            return Response({'Message': 'Invalid refresh token', 'error': str(error_token)},status=status.HTTP_400_BAD_REQUEST)

# TODO: Editorial Detail
        
# TODO: Editorial Delete
        
# TODO: Editorial List