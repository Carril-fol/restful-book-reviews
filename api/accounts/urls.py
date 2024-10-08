from django.urls import path

from .views import *

# Create your URLS here.
urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('activate/<str:token>/', activate_account, name='activate-account')
]