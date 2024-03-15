import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Gender

# Create your tests here.
class GenderCreateTestCase(APITestCase):
    
    def setUp(self):
        self.time_exp = datetime.datetime.now()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.data_gender_test = {
            'name': 'Gender test',
            'synopsis': 'Synopsis test'
        }

    def test_gender_create_view(self):
        refresh_token = RefreshToken.for_user(self.user_admin)

        self.client.cookies['refresh'] = refresh_token
        url_builder_gender = reverse('gender-builder')
        response = self.client.post(url_builder_gender, self.data_gender_test)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gender.objects.get().name, self.data_gender_test['name'])

    def test_gender_create_view_unauthorized(self):
        refresh_token = RefreshToken.for_user(self.user)
        invalid_token_exp = refresh_token.set_exp(self.time_exp)
        self.client.cookies['refresh'] = invalid_token_exp
        
        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)
        self.assertEqual(response_creation_view.status_code, status.HTTP_401_UNAUTHORIZED)


class DetailGenderTestCase(APITestCase):

    def setUp(self):
        self.time_exp = datetime.datetime.now()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.data_gender_test = {
            'name': 'Gender test',
            'synopsis': 'Synopsis test'
        }

    def test_gender_detail_view(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)

        refresh_token_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_user

        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_detail_gender = reverse('gender-detail', kwargs={'gender_id': gender_id})
        response_detail_view = self.client.get(url_detail_gender)
        
        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gender.objects.get().name, self.data_gender_test['name'])
        self.assertEqual(response_detail_view.status_code, status.HTTP_200_OK)

    def test_gender_detail_view_unauthorized(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)
        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)

        refresh_token = RefreshToken.for_user(self.user)
        invalid_token_exp = refresh_token.set_exp(self.time_exp)
        self.client.cookies['refresh'] = invalid_token_exp

        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_detail_gender = reverse('gender-detail', kwargs={'gender_id': gender_id})
        response_detail_view = self.client.get(url_detail_gender)

        self.assertEqual(Gender.objects.get().name, self.data_gender_test['name'])
        self.assertEqual(response_detail_view.status_code, status.HTTP_401_UNAUTHORIZED)


class GenderListTestCase(APITestCase):

    def setUp(self):
        self.time_exp = datetime.datetime.now()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.data_gender_test = {
            'name': 'Gender test',
            'synopsis': 'Synopsis test'
        }

    def test_gender_list(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin
        
        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)

        refresh_token_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_user

        url_gender_list = reverse('gender-list')
        response_gender_list = self.client.get(url_gender_list)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_gender_list.status_code, status.HTTP_200_OK)

    def test_gender_list_unauthorized(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin
        
        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)
        
        refresh_token = RefreshToken.for_user(self.user)
        invalid_token_exp = refresh_token.set_exp(self.time_exp)
        self.client.cookies['refresh'] = invalid_token_exp

        url_gender_list = reverse('gender-list')
        response_gender_list = self.client.get(url_gender_list)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_gender_list.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteGenderTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.data_gender_test = {
            'name': 'Gender test',
            'synopsis': 'Synopsis test'
        }

    def test_gender_delete(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)
        
        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_delete_view = reverse('gender-deleter', kwargs={'gender_id': gender_id})
        response_delete_view = self.client.delete(url_delete_view)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_view.status_code, status.HTTP_200_OK)

    def test_unauthorized_gender_delete(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_delete_view = reverse('gender-deleter', kwargs={'gender_id': gender_id})
        response_delete_view = self.client.delete(url_delete_view)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_view.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateGenderTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.data_gender_test = {
            'name': 'Gender test',
            'synopsis': 'Synopsis test'
        }

    def test_gender_update(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)

        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_update_view = reverse('gender-update', kwargs={'gender_id': gender_id})

        self.data_gender_test.update({'name': 'Gender test updated'})
        response_update_view = self.client.put(url_update_view, self.data_gender_test)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_view.status_code, status.HTTP_200_OK)
        self.assertEqual(response_update_view.data, {'Message': 'The entered gender has been updated.'})
        self.assertEqual(Gender.objects.get().name, 'Gender test updated')

    def test_unauthorized_gender_update(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_update_view = reverse('gender-update', kwargs={'gender_id': gender_id})

        self.data_gender_test.update({'name': 'Gender test updated'})
        response_update_view = self.client.put(url_update_view, self.data_gender_test)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_view.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_update_view.data, {'Error': 'The logged in user does not have the permissions to perform this action.'})