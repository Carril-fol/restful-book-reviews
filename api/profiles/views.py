from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Profile
from .serializers import ProfileSerializer
from accounts.views import TokenDecoder
from reviews.models import Review

# Create your views here.
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
		reviews = Review.objects.filter(user_creator=profile.user.pk)
		reviews_list = []
		for review in reviews:
			review_data = {
				'id': review.pk,
				'comment': review.comment,
				'stars': review.stars,
				'likes': review.likes_count()
            }
			reviews_list.append(review_data)	
		profile_data = {
			'first_name': profile.first_name,
			'last_name': profile.last_name,
			'img_profile': profile.img_profile.url,
			'user': profile.user.pk,
			'reviews': reviews_list
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
		
		if profile.user.pk != user_id:
			return Response({'Message': 'The ID entered not belong to the user creator.'}, status=status.HTTP_401_UNAUTHORIZED)
		
		serializer = ProfileSerializer(instance=profile, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'Message': 'Profile updated'}, status=status.HTTP_200_OK)
		return Response({'Message': 'Error to update the profile', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)