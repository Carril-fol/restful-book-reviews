from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Profile
from accounts.views import TokenDecoder
from .serializers import ProfileSerializer

# Create your views here.
"""
Profile
"""
class ProfileDetail(APIView):
	authentication_classes = (JWTAuthentication,)

	def get(self, request):
		token_decoder = TokenDecoder()
		raw_token = request.COOKIES.get('refresh')
		if not raw_token:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		user_id = token_decoder.decode_token(raw_token)
		if user_id is None:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		
        # TODO: Fix try and except
		try:
			get_profile = get_object_or_404(Profile, id=user_id)
			profile_data = {
				'first_name': get_profile.first_name,
				'last_name': get_profile.last_name,
				'img_profile': get_profile.img_profile.url,
				'user': get_profile.user.pk
			}
			return Response({'User data': profile_data}, status=status.HTTP_200_OK)
		except get_profile.DoesNotExist:
			return Response({}, status=status.HTTP_404_NOT_FOUND)
		

class ProfileUpdate(APIView):
	authentication_classes = (JWTAuthentication,)

	def put(self, request):
		token_decoder = TokenDecoder()
		raw_token = request.COOKIES.get('refresh')
		if not raw_token:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		user_id = token_decoder.decode_token(raw_token)
		if user_id is None:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		
        # TODO: Make try and except
		profile_id = get_object_or_404(Profile, id=user_id)

		if profile_id.user.pk == user_id:
			serializer = ProfileSerializer(data=request.data, instance=profile_id)
			if serializer.is_valid():
				serializer.save()
				return Response({'message': 'Profile updated'}, status=status.HTTP_200_OK)
			return Response({'message': 'Error to update the task', 'error': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
		return Response({'message': 'the entered object ID does not belong to the user'}, status=status.HTTP_401_UNAUTHORIZED)

