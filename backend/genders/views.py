from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.views import TokenDecoder
from books.models import Book

from .models import Gender
from .serializers import GenderSerializer


# Create your views here.
class GenderCreate(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            admin_user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not (admin_user_instance.is_superuser or admin_user_instance.is_staff):
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Gender created.'}, status=status.HTTP_201_CREATED)



class GenderDetail(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, gender_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'No user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({'Error': 'There is no gender introduced'}, status=status.HTTP_404_NOT_FOUND)
        
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
        gender_data = {
            'gender': gender.name,
            'synopsis': gender.synopsis
        }
        return Response({'Gender data': gender_data, 'Books with that gender': books_list}, status=status.HTTP_200_OK)



class GenderList(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            admin_user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if not (admin_user_instance.is_superuser or admin_user_instance.is_staff):
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        genders = Gender.objects.all()
        genders_data_list = []
        if genders:
            for gender in genders:
                gender_data = {
                    'id': gender.pk,
                    'name': gender.name,
                    'synopsis': gender.synopsis
                }
                genders_data_list.append(gender_data)
            return Response({'Genders': genders_data_list}, status=status.HTTP_200_OK)
        return Response({'Error': 'There are no literary genders created at this time in the database.'}, status=status.HTTP_404_NOT_FOUND)


class GenderDelete(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request, gender_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            admin_user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({'Error': 'There is no gender introduced'}, status=status.HTTP_404_NOT_FOUND)

        if not( admin_user_instance.is_staff or admin_user_instance.is_superuser):
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)

        gender.delete()
        return Response({'Message': 'The entered gender is deleted.'}, status=status.HTTP_200_OK)



class GenderUpdate(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, gender_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            admin_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'The user entered does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({'Error': 'There is no gender introduced'}, status=status.HTTP_404_NOT_FOUND)

        if not (admin_user.is_staff or admin_user.is_superuser):
            return Response({'Error': 'The logged in user does not have the permissions to perform this action.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = GenderSerializer(instance=gender, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'The entered gender has been updated.'}, status=status.HTTP_200_OK)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
