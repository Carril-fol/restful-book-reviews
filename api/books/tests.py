import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from genders.models import Gender
from publishers.models import Publisher
from .models import Book

# Create your tests here.

class PublishBookTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username test',
            password='password test'
        )
        self.admin = User.objects.create_superuser(
            username='username admin test', 
            password='password admin test'
        )
        self.publisher_test = Publisher.objects.create(
            name='Publisher test'
        )
        self.gender_test = Gender.objects.create(
            name='Gender test', 
            synopsis='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
        )
        self.book_data = {
            'title': 'Title test',
            'subtitle' : 'Sub title test',
            'isbn': 1234567890123,
            'author': 'Test author',
            'publication_date': datetime.datetime.today().date(),
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
            'editorial': self.publisher_test.pk,
            'gender': self.gender_test.pk
        }

    def test_publish_book(self):
        refresh_token_admin = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token_admin
        
        url = reverse('book-builder')
        response_publish_book = self.client.post(url, self.book_data)

        self.assertEqual(response_publish_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.get().title, self.book_data['title'])


class AllBooksListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username test',
            password='password test'
        )
        self.admin = User.objects.create_superuser(
            username='username admin test', 
            password='password admin test'
        )
        self.publisher_test = Publisher.objects.create(
            name='Publisher test'
        )
        self.gender_test = Gender.objects.create(
            name='Gender test', 
            synopsis='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
        )
        self.book_data = {
            'title': 'Title test',
            'subtitle' : 'Sub title test',
            'isbn': 1234567890123,
            'author': 'Test author',
            'publication_date': datetime.datetime.today().date(),
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
            'editorial': self.publisher_test.pk,
            'gender': self.gender_test.pk
        }

    def test_all_books_list(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token_admin_user
        url_book_builder = reverse('book-builder')
        response_book_builder = self.client.post(url_book_builder, self.book_data)
        
        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user
        url_all_books = reverse('all-books')
        response_all_books_list = self.client.get(url_all_books)
        
        self.assertEqual(response_book_builder.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.get().title, self.book_data['title'])
        self.assertEqual(response_all_books_list.status_code, status.HTTP_200_OK)

    def test_not_books_in_the_database(self):
        refresh_token = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token

        url_all_books = reverse('all-books')
        response_all_books_list = self.client.get(url_all_books)
        self.assertEqual(response_all_books_list.status_code, status.HTTP_200_OK)
        self.assertEqual(response_all_books_list.data, {'All Books': []})


class AllBooksWithGendeSpecific(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='username test',
            password='password test'
        )
        self.admin = User.objects.create_superuser(
            username='username admin test', 
            password='password admin test'
        )
        self.publisher_test = Publisher.objects.create(
            name='Publisher test'
        )
        self.gender_test = Gender.objects.create(
            name='Gender test', 
            synopsis='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
        )
        self.book_data = {
            'title': 'Title test',
            'subtitle' : 'Sub title test',
            'isbn': 1234567890123,
            'author': 'Test author',
            'publication_date': datetime.datetime.today().date(),
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
            'editorial': self.publisher_test.pk,
            'gender': self.gender_test.pk
        }

    def test_list_book_with_specific_gender(self):
        refresh_token = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token

        gender_id = Gender.objects.get(name='Gender test').pk
        url_list_books_specific_gender = reverse('books-specific-gender', kwargs={'gender_id': gender_id})        
        response_list_book_specific_gender = self.client.get(url_list_books_specific_gender)
        
        self.assertEqual(response_list_book_specific_gender.status_code, status.HTTP_200_OK)


class DetailBookTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username test',
            password='password test'
        )
        self.admin = User.objects.create_superuser(
            username='username admin test', 
            password='password admin test'
        )
        self.publisher_test = Publisher.objects.create(
            name='Publisher test'
        )
        self.gender_test = Gender.objects.create(
            name='Gender test', 
            synopsis='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
        )
        self.book_data = {
            'title': 'Title test',
            'subtitle' : 'Sub title test',
            'isbn': 1234567890123,
            'author': 'Test author',
            'publication_date': datetime.datetime.today().date(),
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
            'editorial': self.publisher_test.pk,
            'gender': self.gender_test.pk
        }

    def test_detail_book(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token_admin_user
        url_book_builder = reverse('book-builder')
        response_book_builder = self.client.post(url_book_builder, self.book_data)
        

        book_id = Book.objects.get(title=self.book_data['title']).pk
        url_detail_book = reverse('detail-book', kwargs={'book_id': book_id})
        response_detail_book = self.client.get(url_detail_book)

        self.assertEqual(response_book_builder.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_book.status_code, status.HTTP_200_OK)


class DeleteBookTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username test',
            password='password test'
        )
        self.admin = User.objects.create_superuser(
            username='username admin test', 
            password='password admin test'
        )
        self.publisher_test = Publisher.objects.create(
            name='Publisher test'
        )
        self.gender_test = Gender.objects.create(
            name='Gender test', 
            synopsis='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
        )
        self.book_data = {
            'title': 'Title test',
            'subtitle' : 'Sub title test',
            'isbn': 1234567890123,
            'author': 'Test author',
            'publication_date': datetime.datetime.today().date(),
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
            'editorial': self.publisher_test.pk,
            'gender': self.gender_test.pk
        }

    def test_delete_book(self):
        refresh_token = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token

        url_builder_book = reverse('book-builder')
        response_builder_book = self.client.post(url_builder_book, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        url_delete_book = reverse('delete-book', kwargs={'book_id': book_id})
        response_delete_book = self.client.delete(url_delete_book)

        self.assertEqual(response_builder_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_book.status_code, status.HTTP_200_OK)
        self.assertEqual(response_delete_book.data, {'Message': 'Book deleted.'})

    def test_unauthorized_delete_book(self):
        refresh_token = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token

        url_builder_book = reverse('book-builder')
        response_builder_book = self.client.post(url_builder_book, self.book_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        book_id = Book.objects.get(title=self.book_data['title']).pk
        url_delete_book = reverse('delete-book', kwargs={'book_id': book_id})
        response_delete_book = self.client.delete(url_delete_book)
        
        self.assertEqual(response_builder_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_book.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_delete_book.data, {'Message': 'The logged in user does not have permissions to do this.'})


class UpdateBookTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='username test',
            password='password test'
        )
        self.admin = User.objects.create_superuser(
            username='username admin test', 
            password='password admin test'
        )
        self.publisher_test = Publisher.objects.create(
            name='Publisher test'
        )
        self.gender_test = Gender.objects.create(
            name='Gender test', 
            synopsis='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum'
        )
        self.book_data = {
            'title': 'Title test',
            'subtitle' : 'Sub title test',
            'isbn': 1234567890123,
            'author': 'Test author',
            'publication_date': datetime.datetime.today().date(),
            'synopsis': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum',
            'editorial': self.publisher_test.pk,
            'gender': self.gender_test.pk
        }

    def test_update_book(self):
        refresh_token_admin = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_book_builder = reverse('book-builder')
        response_publish_book = self.client.post(url_book_builder, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        url_update_book = reverse('book-updater', kwargs={'book_id': book_id})

        updated_book_dict = self.book_data.update({'title': 'Title updated'})
        response_update_book = self.client.put(url_update_book, updated_book_dict)

        self.assertEqual(response_publish_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_book.status_code, status.HTTP_200_OK)


    def test_unauthorized_update_book(self):
        refresh_token_admin = RefreshToken.for_user(self.admin)
        self.client.cookies['refresh'] = refresh_token_admin

        url_book_builder = reverse('book-builder')
        response_publish_book = self.client.post(url_book_builder, self.book_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        book_id = Book.objects.get(title=self.book_data['title']).pk
        url_update_book = reverse('book-updater', kwargs={'book_id': book_id})

        updated_book_dict = self.book_data.update({'title': 'Title updated'})
        response_update_book = self.client.put(url_update_book, updated_book_dict)

        self.assertEqual(response_publish_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_book.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_update_book.data, {'Message': 'The logged in user does not have permissions to do this.'})