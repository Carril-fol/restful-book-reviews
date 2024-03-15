from django.urls import path

from .views import *

# Create your URLS here.
urlpatterns = [
    path(
      'api/book-publish/',
      PublishBook.as_view(),
      name='book-builder'
    ),
    path(
      'api/books/',
      AllBooksList.as_view(),
      name='all-books'
    ),
    path(
      'api/books/gender/<int:gender_id>/',
      ListBookSpecificGender.as_view(),
      name='books-specific-gender'
    ),
    path(
      'api/detail/book/<int:book_id>/',
      DetailBook.as_view(),
      name='detail-book'
    ),
    path(
      'api/delete/book/<int:book_id>/',
      DeleteBook.as_view(),
      name='delete-book'
    ),
    path(
      'api/update/book/<int:book_id>/',
      UpdateBook.as_view(),
      name='book-updater'
    )
]
