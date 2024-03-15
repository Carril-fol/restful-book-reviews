from django.urls import path

from .views import *

urlpatterns = [
    path(
      'api/build-publisher/',
      CreatePublisher.as_view(),
      name='builder-publisher'
    ),
    path(
      'api/detail/publisher/<int:publisher_id>/',
      DetailPublisher.as_view(),
      name='detail-publisher'
    ),
    path(
      'api/delete/publisher/<int:publisher_id>/',
      DeletePublisher.as_view(),
      name='delete-publisher'
    ),
    path(
      'api/update/publisher/<int:publisher_id>/',
      UpdatePublisher.as_view(),
      name='update-publisher'
    ),
    path(
      'api/books/publisher/<int:publisher_id>/',
      ListBooksPublisher.as_view(),
      name='list-books-publisher'
    )
]
