from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import isVerified
from reviews.models import Review

from .permissions import hisProfile
from .models import Profile
from .serializers import UpdateProfileSerializer

# Create your views here.
class ProfileDetail(APIView):
    """
    Example:

    GET: api/profile/detail/<int:profile_id>/

    ```
    Successful response (code 200 - OK):
    {
        'User data': {
            'username': profile.user.username,
            'bio': profile.bio,
            'location': profile.location,
            'followers': profile.followers,
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'img_profile': profile.img_profile.url,
            'user': profile.user.pk,
            'reviews': reviews_list
        }
    }

    Response with validation errors (code 404 - Not Found):
    {
        'Message': 'The ID entered does not belong to any user profile.'
    }
    ```
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request, profile_id):
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
            'username': profile.user.username,
            'bio': profile.bio,
            'location': profile.location,
            'followers': profile.followers,
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'img_profile': profile.img_profile.url,
            'user': profile.user.pk,
            'reviews': reviews_list
        }
        return Response({'User data': profile_data}, status=status.HTTP_200_OK)


class ProfileUpdate(APIView):
    """
    Example:

    PUT: api/profile-update/<int:profile_id>/

    ```
    Aplication data:
    {
        'username': 'New username for the user',
        'first_name': 'New first name for the user',
        'last_name': 'New last name for the user',
        'bio': 'New bio for the profile',
        'location': 'New location for the profile',
        'img_profile': 'New image profile for the profile'
    }

    Successful response (code 200 - OK):
    {
        "Message": "Profile updated"
    }

    Response with validation errors (code 400 - Bad Requests):
    {
        "Error": {
            'username': ['The username cannot be incomplete...'],
            'first_name': ['The name cannot be incomplete...']
            // Other errors of validation from the serializer.
        }
    }
    ```
    """
    serializer_class = UpdateProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified, hisProfile]

    def put(self, request, profile_id):
        try:
            profile = Profile.objects.get(id=profile_id)
        except Profile.DoesNotExist:
            return Response({'Message': 'The ID entered does not belong to any user profile.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = self.serializer_class(instance=profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Profile updated'}, status=status.HTTP_200_OK)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# TODO: Make function to follow profiles.