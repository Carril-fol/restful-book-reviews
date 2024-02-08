from django.urls import path

from .views import *

urlpatterns = [
    path(
      'api/profile/detail/',
      ProfileDetail.as_view(),
      name='profile-detail'
    ),
    path(
      'api/profile-update/',
      ProfileUpdate.as_view(),
      name='profile-update'
    )
]
