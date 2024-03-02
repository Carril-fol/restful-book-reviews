import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import Publisher

# Create your tests here.

class CreatePublisherTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.publisher_data = {
            'name': 'Test publisher'
        }

    def test_create_publisher(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        
    def test_create_publisher_unauthorized(self):
        refresh_token = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        self.assertEqual(response_publisher_create.status_code, status.HTTP_401_UNAUTHORIZED)


class DetailPublisherTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.publisher_data = {
            'name': 'Test publisher'
        }

    def test_detail_publisher(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user
        
        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        url_detail_publisher = reverse('detail-publisher', kwargs={'publisher_id': publisher_id})
        response_detail_publisher = self.client.get(url_detail_publisher)

        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_publisher.status_code, status.HTTP_200_OK)

    def test_detail_publisher_unauthorized(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        self.client.cookies['refresh'] = ''
        
        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        url_detail_publisher = reverse('detail-publisher', kwargs={'publisher_id': publisher_id})
        response_detail_publisher = self.client.get(url_detail_publisher)

        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_publisher.status_code, status.HTTP_401_UNAUTHORIZED)


class DeletePublisherTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.publisher_data = {
            'name': 'Test publisher'
        }

    def test_delete_publisher(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        url_delete_publisher = reverse('delete-publisher', kwargs={'publisher_id': publisher_id})
        response_publisher_delete = self.client.delete(url_delete_publisher)
        
        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_publisher_delete.status_code, status.HTTP_200_OK)

    def test_delete_publisher_unauthorized(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        url_delete_publisher = reverse('delete-publisher', kwargs={'publisher_id': publisher_id})
        response_publisher_delete = self.client.delete(url_delete_publisher)
        
        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_publisher_delete.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdatePublisherTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.publisher_data = {
            'name': 'Test publisher'
        }

    def test_update_publisher(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        self.publisher_data.update({'name': 'Name updated'})
        url_update_publisher = reverse('update-publisher', kwargs={'publisher_id': publisher_id})
        response_update_publisher = self.client.put(url_update_publisher, self.publisher_data)
        
        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_publisher.status_code, status.HTTP_200_OK)

    def test_update_publisher_unauthorized(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        self.publisher_data.update({'name': 'Name updated'})
        url_update_publisher = reverse('update-publisher', kwargs={'publisher_id': publisher_id})
        response_update_publisher = self.client.put(url_update_publisher, self.publisher_data)
        
        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_publisher.status_code, status.HTTP_401_UNAUTHORIZED)


class ListBookPublisherTestCase(APITestCase):

    def setUp(self):
        self.time_exp = datetime.datetime.now()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_admin = User.objects.create_superuser(username='admintestuser', password='admintest')
        self.publisher_data = {
            'name': 'Test publisher'
        }

    def test_list_books_publishers(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        url_list_books_publisher = reverse('list-books-publisher', kwargs={'publisher_id': publisher_id})
        response_list_books = self.client.get(url_list_books_publisher)

        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_list_books.status_code, status.HTTP_200_OK)

    def test_list_books_publishers_token_expired(self):
        refresh_token_admin = RefreshToken.for_user(self.user_admin)
        self.client.cookies['refresh'] = refresh_token_admin
        url_publisher_create = reverse('builder-publisher')
        response_publisher_create = self.client.post(url_publisher_create, self.publisher_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        token_expired = refresh_token_common_user.set_exp(self.time_exp)
        self.client.cookies['refresh'] = token_expired

        publisher_id = Publisher.objects.get(name=self.publisher_data['name']).pk
        url_list_books_publisher = reverse('list-books-publisher', kwargs={'publisher_id': publisher_id})
        response_list_books = self.client.get(url_list_books_publisher)

        self.assertEqual(response_publisher_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_list_books.status_code, status.HTTP_401_UNAUTHORIZED)