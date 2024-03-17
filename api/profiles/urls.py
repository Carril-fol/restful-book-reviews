from django.urls import path

from .views import *

urlpatterns = [
    path('api/profile/detail/<int:profile_id>/', ProfileDetail.as_view(), name='profile-detail'),
    path('api/profile-update/<int:profile_id>/', ProfileUpdate.as_view(),name='profile-update')
]
