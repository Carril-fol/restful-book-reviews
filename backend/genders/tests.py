from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Gender

# Create your tests here.
class GenderTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.data_gender_test = {
            'name': 'Gender test',
            'synopsis': 'Synopsis test'
        }
        self.data_gender_test_update = {
            'name': 'Gender test updated',
            'synopsis': 'Synopsis test updated'  
        }

    def test_gender_create_view(self):
        # TODO: Make the documentation 

        refresh_token = RefreshToken.for_user(self.user_admin)

        self.client.cookies['refresh'] = refresh_token
        url_builder_gender = reverse('gender-builder')
        response = self.client.post(url_builder_gender, self.data_gender_test)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Gender.objects.get().name, self.data_gender_test['name'])

    def test_gender_detail_view(self):
        # TODO: Make the documentation 

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

    def test_gender_list(self):
        # TODO: Make the documentation 

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

    def test_gender_delete(self):
        # TODO: Make the documentation 

        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)
        
        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_delete_view = reverse('gender-deleter', kwargs={'gender_id': gender_id})
        response_delete_view = self.client.delete(url_delete_view)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_view.status_code, status.HTTP_200_OK)

    def test_gender_update(self):
        # TODO: Make the documentation 

        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_builder_gender = reverse('gender-builder')
        response_creation_view = self.client.post(url_builder_gender, self.data_gender_test)

        gender_id = Gender.objects.get(name=self.data_gender_test['name']).pk
        url_update_view = reverse('gender-update', kwargs={'gender_id': gender_id})
        response_update_view = self.client.put(url_update_view, self.data_gender_test_update)

        self.assertEqual(response_creation_view.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_view.status_code, status.HTTP_200_OK)
        self.assertEqual(Gender.objects.get().name, self.data_gender_test_update['name'])