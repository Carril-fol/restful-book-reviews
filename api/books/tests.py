import datetime

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from accounts.views import TokenView
from genders.models import Gender
from .models import Book

# Create your tests here.