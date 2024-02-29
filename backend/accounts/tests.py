import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from profiles.models import Profile

# Create your tests here.

class AccountsTestsCase(APITestCase):
    
    def setUp(self):
        self.account_data = {
            "username": "username test",
            "password": "passwordtest",
            "password2": "passwordtest",
            "first_name": "Test",
            "last_name": "Case",
            "email": "test@gmail.com"
        }
        self.login_data = {
            'username': self.account_data['username'],
            'password': self.account_data['password']
        }

    def test_register_view(self):
        url = reverse('register')
        response = self.client.post(url, self.account_data)
        user_id = User.objects.get(username='username test').pk
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.get().user.pk, user_id)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.account_data = {
            "username": "username test",
            "password": "passwordtest",
            "password2": "passwordtest",
            "first_name": "Test",
            "last_name": "Case",
            "email": "test@gmail.com"
        }
        self.login_data = {
            'username': self.account_data['username'],
            'password': self.account_data['password']
        }

    def test_login_view(self):
        url_register = reverse('register')
        url_login = reverse('login')
        response_register = self.client.post(url_register, self.account_data)
        response_login = self.client.post(url_login, self.login_data)
        
        self.assertEqual(response_register.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_login.data)
        self.assertIn('refresh', response_login.data)


class LogoutViewTestCase(APITestCase):

    def setUp(self):
        self.time_exp = datetime.datetime.now()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.refresh_token = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = self.refresh_token

    def test_logout_successful(self):
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_unsuccesful(self):
        self.client.cookies['refresh'] = ''

        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_token_invalid(self):
        refresh_token = RefreshToken.for_user(self.user)
        invalid_token_exp = refresh_token.set_exp(self.time_exp)
        self.client.cookies['refresh'] = invalid_token_exp

        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)