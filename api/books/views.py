from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import isVerified, isAdminCustom
from genders.models import Gender
from reviews.models import Review

from .serializers import BookSerializer
from .models import Book

# Create your views here.
class PublishBook(APIView):
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdminCustom]
    
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Book published.'}, status=status.HTTP_201_CREATED)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AllBooksList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]
    
    def get(self, request):
        books = Book.objects.all()
        books_list = []
        for book in books:
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
                'gender': gender_data
            }
            books_list.append(book_data)
        return Response({'All Books': books_list}, status=status.HTTP_200_OK)


class ListBookSpecificGender(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request, gender_id):
        try:
            gender = Gender.objects.get(id=gender_id).pk
        except Gender.DoesNotExist:
            return Response({'Message': 'There is no literary gender associated with this ID.'}, status=status.HTTP_404_NOT_FOUND)
        books_gender = Book.objects.filter(gender=gender)
        book_list = []
        for book in books_gender:
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
                'gender': gender_data
            }
            book_list.append(book_data)
        return Response({'Books': book_list}, status=status.HTTP_200_OK)
        

class DetailBook(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'No book is associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        reviews = Review.objects.filter(book=book.pk)
        reviews_list = []
        for review in reviews:
            review_data = {
                'id': review.pk,
                'comment': review.comment,
                'stars': review.stars,
                'likes': review.likes_count(),
                'author_review': review.user_creator.pk,
                'book': review.book.pk
            }
            reviews_list.append(review_data)      
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
            'gender': gender_data,
            'reviews': reviews_list
        }
        return Response({'Book': book_data}, status=status.HTTP_200_OK)


class DeleteBook(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdminCustom]

    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response({'Message': 'Book deleted.'}, status=status.HTTP_200_OK)


class UpdateBook(APIView):
    serializer_class = BookSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdminCustom]

    def put(self, request, book_id):
        try:
            book_instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'No book is associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        serializer = self.serializer_class(instance=book_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Book updated.'}, status=status.HTTP_200_OK)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)