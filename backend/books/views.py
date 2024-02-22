from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.views import TokenDecoder
from genders.models import Gender
from reviews.models import Review

from .serializers import BookSerializer
from .models import Book


# Create your views here.
class PublishBook(APIView):
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
            return Response({'Error': 'No user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        if not (admin_user_instance.is_staff or admin_user_instance.is_superuser):
            return Response({'Error': 'The user does not have permissions for these actions.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Book published.'}, status=status.HTTP_201_CREATED)
        return Response({'Message': 'Error to publish a book', 'Detail book': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AllBooksList(APIView):
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
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'No user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        books = Book.objects.all()
        if not books:
            return Response({'Message': 'No books for the moment.'}, status=status.HTTP_404_NOT_FOUND)

        books_list = []
        for book in books:
            editorial_data = {
                'id': book.editorial.pk,
                'name': book.editorial.name
            }
            gender_data = {
                'id': book.gender.pk,
                'name': book.gender.name,
                'synopsis': book.gender.synopsis
            }
            book_data = {
                'id': book.pk,
                'title': book.title,
                'subtitle': book.subtitle,
                'isbn': book.isbn,
                'author': book.author,
                'publication_date': book.publication_date,
                'synopsis': book.synopsis,
                'editorial': editorial_data,
                'gender': gender_data
            }
            books_list.append(book_data)
        return Response({'All Books': books_list}, status=status.HTTP_200_OK)


class ListBookGenderSpecificGender(APIView):
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
            gender = get_object_or_404(Gender, id=gender_id)
        except Gender.DoesNotExist:
            return Response({'Message': 'There is no literary gender associated with this ID.'}, status=status.HTTP_404_NOT_FOUND)

        books_gender = Book.objects.filter(gender=gender)
        if not books_gender:
            return Response({'Message': 'There are no books associated with this gender ID.'}, status=status.HTTP_404_NOT_FOUND)
            
        book_list = []
        for book in books_gender:
            editorial_data = {
                'id': book.editorial.pk,
                'name': book.editorial.name
            }
            gender_data = {
                'id': book.gender.pk,
                'name': book.gender.name,
                'synopsis': book.gender.synopsis
            }
            book_data = {
                'id': book.pk,
                'title': book.title,
                'subtitle': book.subtitle,
                'isbn': book.isbn,
                'author': book.author,
                'publication_date': book.publication_date,
                'synopsis': book.synopsis,
                'editorial': editorial_data,
                'gender': gender_data
            }
            book_list.append(book_data)
        return Response({'Books': book_list}, status=status.HTTP_200_OK)
        

class DetailBook(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, book_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'No book is associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(book=book)
        reviews_list = []
        for review in reviews:
            likes_ids = list(review.likes.values_list('id', flat=True))
            review_data = {
                'id': review.pk,
                'comment': review.comment,
                'stars': review.stars,
                'likes': likes_ids,
                'author_review': review.user_creator.pk,
                'book': review.book.pk
            }
            reviews_list.append(review_data)      
        editorial_data = {
            'id': book.editorial.pk,
            'name': book.editorial.name
        }
        gender_data = {
            'id': book.gender.pk,
            'name': book.gender.name,
            'synopsis': book.gender.synopsis
        }
        book_data = {
            'id': book.pk,
            'title': book.title,
            'subtitle': book.subtitle,
            'isbn': book.isbn,
            'author': book.author,
            'publication_date': book.publication_date,
            'synopsis': book.synopsis,
            'editorial': editorial_data,
            'gender': gender_data,
            'reviews': reviews_list
        }
        return Response({'Book': book_data}, status=status.HTTP_200_OK)


class DeleteBook(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request, book_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            admin_user = get_object_or_404(User, id=user_id)
        except User.DoesNotExist:
            return Response({'Error': 'No user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not (admin_user.is_superuser or admin_user.is_staff):
            return Response({'Message': 'The logged in user does not have permissions to do this.'}, status=status.HTTP_401_UNAUTHORIZED)

        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response({'Message': 'Book deleted.'}, status=status.HTTP_200_OK)



class UpdateBook(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, book_id):
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
            return Response({'Error': 'No user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            book_instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'No book is associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)

        if not (admin_user_instance.is_superuser or admin_user_instance.is_staff):
            return Response({'Message': 'The logged in user does not have permissions to do this.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = BookSerializer(instance=book_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Book updated.'}, status=status.HTTP_200_OK)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)