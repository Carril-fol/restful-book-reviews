import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile

# Create your tests here.
class ProfileDetailTestCase(APITestCase):
    
    def setUp(self):
        self.time_exp = datetime.datetime.today().date()
        self.account_data = {
            "username": "username test",
            "password": "passwordtest",
            "password2": "passwordtest",
            "first_name": "Test",
            "last_name": "Case",
            "email": "test@gmail.com"
        }

    def test_detail_profile(self):
        url = reverse('register')
        response_register_view = self.client.post(url, self.account_data)
        user_id = User.objects.get(username='username test')
        
        refresh_token_common_user = RefreshToken.for_user(user_id)
        self.client.cookies['refresh'] = refresh_token_common_user
        profile_id = Profile.objects.get(user=user_id.pk).pk
        url_detail_view = reverse('profile-detail', kwargs={'profile_id': profile_id})
        response_detail_view = self.client.get(url_detail_view)

        self.assertEqual(response_register_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_view.status_code, status.HTTP_200_OK)

    def test_detail_profile_token_expired(self):
        url = reverse('register')
        response_register_view = self.client.post(url, self.account_data)
        user_id = User.objects.get(username='username test')
        
        refresh_token_common_user = RefreshToken.for_user(user_id)
        token_expired = refresh_token_common_user.set_exp(self.time_exp)
        self.client.cookies['refresh'] = token_expired
        profile_id = Profile.objects.get(user=user_id.pk).pk
        url_detail_view = reverse('profile-detail', kwargs={'profile_id': profile_id})
        response_detail_view = self.client.get(url_detail_view)

        self.assertEqual(response_register_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_view.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileUpdateTestCase(APITestCase):

    def setUp(self):
        self.time_exp = datetime.datetime.today().date()
        self.user_not_creator = User.objects.create_user(username='User test not creator', password='passwordtest')
        self.account_data = {
            "username": "username test",
            "password": "passwordtest",
            "password2": "passwordtest",
            "first_name": "Test",
            "last_name": "Case",
            "email": "test@gmail.com"
        }

    def test_update_profile(self):
        url_register_view = reverse('register')
        response_register_view = self.client.post(url_register_view, self.account_data)
        user = User.objects.get(username='username test')
        profile = Profile.objects.get(user=user.pk)

        profile_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'user': profile.user.pk
        }

        refresh_token_common_user = RefreshToken.for_user(user)
        self.client.cookies['refresh'] = refresh_token_common_user
        url_update_view = reverse('profile-update', kwargs={'profile_id': profile.pk})
        profile_data.update({'last_name': 'case updated'})
        response_update_view = self.client.put(url_update_view, profile_data)
        
        self.assertEqual(response_register_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_view.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.get().last_name, 'Case updated')

    def test_update_profile_unauthorized(self):
        url_register_view = reverse('register')
        response_register_view = self.client.post(url_register_view, self.account_data)
        user = User.objects.get(username='username test')
        profile = Profile.objects.get(user=user.pk)

        profile_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'user': profile.user.pk
        }

        refresh_token_not_user_creator = RefreshToken.for_user(self.user_not_creator)
        self.client.cookies['refresh'] = refresh_token_not_user_creator

        url_update_view = reverse('profile-update', kwargs={'profile_id': profile.pk})
        profile_data.update({'last_name': 'case updated'})
        response_update_view = self.client.put(url_update_view, profile_data)
        
        self.assertEqual(response_register_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_view.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_profile_token_expired(self):
        url_register_view = reverse('register')
        response_register_view = self.client.post(url_register_view, self.account_data)
        user = User.objects.get(username='username test')
        profile = Profile.objects.get(user=user.pk)

        profile_data = {
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'user': profile.user.pk
        }

        refresh_token_user_creator = RefreshToken.for_user(self.user_not_creator)
        token_expired = refresh_token_user_creator.set_exp(self.time_exp)
        self.client.cookies['refresh'] = token_expired

        url_update_view = reverse('profile-update', kwargs={'profile_id': profile.pk})
        profile_data.update({'last_name': 'case updated'})
        response_update_view = self.client.put(url_update_view, profile_data)
        
        self.assertEqual(response_register_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_view.status_code, status.HTTP_401_UNAUTHORIZED)
