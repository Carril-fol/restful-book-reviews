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
	authentication_classes = [JWTAuthentication]

	def get(self, request, profile_id):
		token_decoder = TokenDecoder()
		raw_token = request.COOKIES.get('refresh')
		if not raw_token:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		user_id = token_decoder.decode_token(raw_token)
		if user_id is None:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		
		try:
			profile = Profile.objects.get(id=profile_id)
		except Profile.DoesNotExist:
			return Response({'Message': 'The ID entered does not belong to any user profile.'}, status=status.HTTP_404_NOT_FOUND)
		
		profile_data = {
			'first_name': profile.first_name,
			'last_name': profile.last_name,
			'img_profile': profile.img_profile.url,
			'user': profile.user.pk
		}
		return Response({'User data': profile_data}, status=status.HTTP_200_OK)
		

class ProfileUpdate(APIView):
	authentication_classes = [JWTAuthentication]

	def put(self, request, profile_id):
		token_decoder = TokenDecoder()
		raw_token = request.COOKIES.get('refresh')
		if not raw_token:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		user_id = token_decoder.decode_token(raw_token)
		if user_id is None:
			return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
		
		try:
			profile = Profile.objects.get(id=profile_id)
		except Profile.DoesNotExist:
			return Response({'Message': 'The ID entered does not belong to any user profile.'}, status=status.HTTP_404_NOT_FOUND)

		serializer = ProfileSerializer(data=request.data, instance=profile.pk)
		if serializer.is_valid():
			serializer.save()
			return Response({'Message': 'Profile updated'}, status=status.HTTP_200_OK)
		return Response({'Message': 'Error to update the profile', 'error': serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)