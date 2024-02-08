from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import TokenError
from rest_framework.permissions import IsAdminUser

from accounts.views import TokenDecoder

from .serializers import BookSerializer, GenderSerializer
from .models import Gender, Book

# Create your views here.
class GenderCreate(APIView):
    authentication_classes = (JWTAuthentication, IsAdminUser,)

    def post(self, request):
        try:
            token_decoder = TokenDecoder()
            raw_token = request.COOKIES.get('refresh')
            if not raw_token:
                return Response({'Error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
            user_id = token_decoder.decode_token(raw_token)
            if user_id is None:
                return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
            admin_user = User.objects.get(id=user_id)
            if admin_user.is_superuser or admin_user.is_staff:
                serializer = GenderSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'Message': 'Gender created.'}, status=status.HTTP_201_CREATED)
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as error_token:
            return Response({'Message': 'Invalid refresh token', 'error': str(error_token)},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class GenderDetail(APIView):
    authentication_classes = (JWTAuthentication,)
    
    def get(self, request, gender_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            gender = get_object_or_404(Gender, id=gender_id)
            gender_data = {
                'gender': gender.name,
                'synopsis': gender.synopsis
            }
            books = Book.objects.filter(gender=gender)
            books_list = []
            for book in books:
                book_data = {
                    'title': book.title,
                    'subtitle': book.subtitle,
                    'isbn': book.isbn,
                    'author': book.author,
                    'publication_date': book.publication_date,
                    'synopsis': book.synopsis,
                    'editorial': book.editorial,
                    'gender': book.gender
                }
                books_list.append(book_data)
            return Response({'Gender data': gender_data, 'Books with that gender': books_list}, status=status.HTTP_200_OK)
        except Gender.DoesNotExist:
            return Response({'Error': 'There is no gender introduced'}, status=status.HTTP_404_NOT_FOUND)


class GenderList(APIView):
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            admin_user = User.objects.get(id=user_id)
            if admin_user.is_superuser or admin_user.is_staff:
                genders = Gender.objects.all()
                genders_data_list = []
                if genders:
                    for gender in genders:
                        gender_data = {
                            'name': gender.name,
                            'synopsis': gender.synopsis
                        }
                        genders_data_list.append(gender_data)
                    return Response({'Genders': genders_data_list}, status=status.HTTP_200_OK)
                return Response({'Error': 'There are no literary genders created at this time in the database.'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class GenderDelete(APIView):
    authentication_classes = (JWTAuthentication, IsAdminUser,)

    def delete(self, request, gender_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            admin_user = User.objects.get(id=user_id)
            if admin_user.is_staff or admin_user.is_superuser:
                gender = get_object_or_404(Gender, id=gender_id)
                gender.delete()
                return Response({'Message': 'The entered gender is deleted.'}, status=status.HTTP_200_OK)
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Gender.DoesNotExist:
            return Response({'Error': 'The introduced gender does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class GenderUpdate(APIView):
    authentication_classes = (JWTAuthentication, IsAdminUser,)

    def update(self, request, gender_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            admin_user = User.objects.get(id=user_id)
            if admin_user.is_staff or admin_user.is_superuser:
                gender = get_object_or_404(Gender, id=gender_id)
                serializer = GenderSerializer(instance=gender, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'Message': 'The entered gender has been updated.'}, status=status.HTTP_200_OK)
                return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Gender.DoesNotExist:
            return Response({'Error': 'The introduced gender does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class PublishBook(APIView):
    authentication_classes = (JWTAuthentication, IsAdminUser,)
    
    def post(self, request):
        try:
            token_decoder = TokenDecoder()
            raw_token = request.COOKIES.get('refresh')
            if not raw_token:
                return Response({'error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
            user_id = token_decoder.decode_token(raw_token)
            if user_id is None:
                return Response({'error': 'Token is not found in cookies.'}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Book published.'}, status=status.HTTP_201_CREATED)
        except TokenError as error_token:
            return Response({'message': 'Invalid refresh token', 'error': str(error_token)},status=status.HTTP_400_BAD_REQUEST)

# TODO: List of books
        
# TODO: Detail of books
        
# TODO: Delete of books for admins
        
# TODO: Update of books for admins
        
