import datetime

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from genders.models import Gender
from publishers.models import Publisher
from books.models import Book
from .models import Review

# Create your tests here.

class PublishReviewTestCase(APITestCase):
    
    def setUp(self):
        self.time_exp = datetime.datetime.today().date()
        self.user = User.objects.create_user(username='User test', password='passwordtest')
        self.admin_user = User.objects.create_superuser(username='Admin user', password='passwordtestadmin')
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
        self.review_data = {
            'comment': 'Comment test',
            'stars': 5,
            'likes': self.user.pk,
            'user_creator': self.user.pk,
            'book': ''
        }

    def test_create_review(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)

    def test_create_review_token_expired(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        token_expired = refresh_token_common_user.set_exp(self.time_exp)
        self.client.cookies['refresh'] = token_expired
        
        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_401_UNAUTHORIZED)


class DeleteReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='User test', password='passwordtest')
        self.user_not_creator = User.objects.create_user(username='User test not creator', password='passwordtest')
        self.admin_user = User.objects.create_superuser(username='Admin user', password='passwordtestadmin')
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
        self.review_data = {
            'comment': 'Comment test',
            'stars': 5,
            'likes': self.user.pk,
            'user_creator': self.user.pk,
            'book': ''
        }

    def test_delete_review(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_common_user

        review_id = Review.objects.latest('id').pk
        url_delete_review = reverse('deleter-review', kwargs={'review_id': review_id})
        response_delete_review = self.client.delete(url_delete_review)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_review.status_code, status.HTTP_200_OK)

    def test_delete_review_unauthorized(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        refresh_token_common_user = RefreshToken.for_user(self.user_not_creator)
        self.client.cookies['refresh'] = refresh_token_common_user

        review_id = Review.objects.latest('id').pk
        url_delete_review = reverse('deleter-review', kwargs={'review_id': review_id})
        response_delete_review = self.client.delete(url_delete_review)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_delete_review.status_code, status.HTTP_401_UNAUTHORIZED)


class ListReviewBookSpecificTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='User test', password='passwordtest')
        self.user_not_creator = User.objects.create_user(username='User test not creator', password='passwordtest')
        self.admin_user = User.objects.create_superuser(username='Admin user', password='passwordtestadmin')
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
        self.review_data = {
            'comment': 'Comment test',
            'stars': 5,
            'likes': self.user.pk,
            'user_creator': self.user.pk,
            'book': ''
        }

    def test_list_reviews_from_specific_book(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        url_list_review = reverse('list-reviews-book', kwargs={'book_id': book_id})
        response_list_review = self.client.get(url_list_review)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_list_review.status_code, status.HTTP_200_OK)


class DetailReviewTestCase(APITestCase):
    
    def setUp(self):
        self.time_exp = datetime.datetime.today().date()
        self.user = User.objects.create_user(username='User test', password='passwordtest')
        self.user_not_creator = User.objects.create_user(username='User test not creator', password='passwordtest')
        self.admin_user = User.objects.create_superuser(username='Admin user', password='passwordtestadmin')
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
        self.review_data = {
            'comment': 'Comment test',
            'stars': 5,
            'likes': self.user.pk,
            'user_creator': self.user.pk,
            'book': ''
        }

    def test_detail_review(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        review_id = Review.objects.latest('id').pk
        url_detail_review = reverse('detail-review', kwargs={'review_id': review_id})
        response_detail_review = self.client.get(url_detail_review)
        
        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_review.status_code, status.HTTP_200_OK)

    def test_detail_review_unauthorized(self):
        refresh_token_admin_user = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token_admin_user

        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        book_id = Book.objects.get(title=self.book_data['title']).pk
        self.review_data.update({'book': book_id})
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        refresh_token_common_user = RefreshToken.for_user(self.user)
        token_expired = refresh_token_common_user.set_exp(self.time_exp)
        self.client.cookies['refresh'] = token_expired

        review_id = Review.objects.latest('id').pk
        url_detail_review = reverse('detail-review', kwargs={'review_id': review_id})
        response_detail_review = self.client.get(url_detail_review)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_detail_review.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateReviewTestCase(APITestCase):

    def setUp(self):
        self.time_exp = datetime.datetime.today().date()

        self.user = User.objects.create_user(username='User test', password='passwordtest')
        self.user_not_creator = User.objects.create_user(username='User test not creator', password='passwordtest')
        self.admin_user = User.objects.create_superuser(username='Admin user', password='passwordtestadmin')
        
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
        self.review_data = {
            'comment': 'Comment test',
            'stars': 5,
            'likes': self.user.pk,
            'user_creator': self.user.pk,
            'book': ''
        }

    def test_update_review(self):
        refresh_token = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token
        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        refresh_token_review_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_review_user
        book_id = Book.objects.latest('id').pk
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        self.review_data.update({'book': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        review_id = Review.objects.latest('id').pk
        self.review_data.update({'comment': 'comment updated test'})
        url_update_review = reverse('updater-review', kwargs={'review_id': review_id})
        response_update_review = self.client.put(url_update_review, self.review_data)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_review.status_code, status.HTTP_200_OK)

    def test_update_review_unauthorized(self):
        refresh_token = RefreshToken.for_user(self.admin_user)
        self.client.cookies['refresh'] = refresh_token
        url_create_book = reverse('book-builder')
        response_create_book = self.client.post(url_create_book, self.book_data)

        refresh_token_review_user = RefreshToken.for_user(self.user)
        self.client.cookies['refresh'] = refresh_token_review_user
        book_id = Book.objects.latest('id').pk
        url_create_review = reverse('builder-review', kwargs={'book_id': book_id})
        self.review_data.update({'book': book_id})
        response_create_review = self.client.post(url_create_review, self.review_data)

        refresh_token_review_not_user_creator = RefreshToken.for_user(self.user_not_creator)
        self.client.cookies['refresh'] = refresh_token_review_not_user_creator

        review_id = Review.objects.latest('id').pk
        self.review_data.update({'comment': 'comment updated test'})
        url_update_review = reverse('updater-review', kwargs={'review_id': review_id})
        response_update_review = self.client.put(url_update_review, self.review_data)

        self.assertEqual(response_create_book.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create_review.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_update_review.status_code, status.HTTP_401_UNAUTHORIZED)