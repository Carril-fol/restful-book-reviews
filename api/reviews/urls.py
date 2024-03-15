from django.urls import path

from .views import *

# Create your URLS here.
urlpatterns = [
    path(
      'api/publish-review/<int:book_id>/',
      PublishReview.as_view(),
      name='builder-review'
    ),
    path(
      'api/delete-review/<int:review_id>/',
      DeleteReview.as_view(),
      name='deleter-review'
    ),
    path(
      'api/update-review/<int:review_id>/',
      UpdateReview.as_view(),
      name='updater-review'
    ),
    path(
      'api/reviews/book/<int:book_id>/',
      ListReviewsBookSpecific.as_view(),
      name='list-reviews-book'
    ),
    path(
      'api/detail/review/<int:review_id>/',
      DetailReview.as_view(),
      name='detail-review'
    )
]
