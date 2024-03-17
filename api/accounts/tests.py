import datetime

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from profiles.models import Profile

from .utils import TokenView
from .models import UserCustom

# Create your tests here.

class RegisterTestCase(APITestCase):
    
    def setUp(self):
        self.account_data = {
            'username': "username",
            'first_name': "First name test",
            'last_name': "Last name test",
            'email': "emailtest@gmail.com",
            'password': "passwordTest123-",
            'confirm_password': "passwordTest123-",
        }

    def test_register_view(self):
        url = reverse('register')
        response = self.client.post(url, self.account_data)
        user_id = UserCustom.objects.last().pk

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"Message": "Email verification send"})
        self.assertEqual(Profile.objects.get().user.pk, user_id)


class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.common_user = UserCustom.objects.create(
            username='username',
            first_name='first test',
            last_name='last test',
            email='emailtest@gmail.com',
            password='passwordTest123-'
        )
        self.admin_user = UserCustom.objects.create_superuser(
            username='user admin',
            first_name='first test',
            last_name='last test',
            email='emailtestadmin@gmail.com',
            password='passwordTest123-'
        )
        self.login_data_common_user = {
            'email': 'emailtest@gmail.com',
            'password': 'passwordTest123-'
        }
        self.login_data_admin_user = {
            'email': 'emailtestadmin@gmail.com',
            'password': 'passwordTest123-'
        }        

    def test_login_user_not_verified(self):
        url = reverse('login')
        response = self.client.post(url, self.login_data_common_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view(self):
        url = reverse('login')
        response = self.client.post(url, self.login_data_admin_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutTestCase(APITestCase):

    def setUp(self):
        self.admin_user = UserCustom.objects.create_superuser(
            username='user admin',
            first_name='first test',
            last_name='last test',
            email='emailtestadmin@gmail.com',
            password='passwordTest123-'
        )
        self.login_data_admin_user = {
            'email': 'emailtestadmin@gmail.com',
            'password': 'passwordTest123-'
        }     

    def test_logout_user(self):
        url_logout = reverse('logout')
        url_login = reverse('login')

        response_login = self.client.post(url_login, self.login_data_admin_user)        
        response_login.set_cookie('access', response_login.data['access'])
        response_login.set_cookie('refresh', response_login.data['refresh'])

        response_logout = self.client.post(url_logout)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertEqual(response_logout.status_code, status.HTTP_200_OK)