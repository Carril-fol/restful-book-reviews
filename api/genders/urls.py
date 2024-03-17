from django.urls import path
from .views import *

# 
urlpatterns = [
    path('api/gender-builder/', GenderCreate.as_view(), name='gender-builder'),
    path('api/gender-detail/<int:gender_id>/', GenderDetail.as_view(), name='gender-detail'),
    path('api/list-genders/', GenderList.as_view(), name='gender-list'),
    path('api/gender-delete/<int:gender_id>/', GenderDelete.as_view(), name='gender-deleter'),
    path('api/gender-update/<int:gender_id>/', GenderUpdate.as_view(), name='gender-update')
]
