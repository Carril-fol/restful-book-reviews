from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import PublisherSerializer
from .models import Publisher

from reviews.models import Review
from books.models import Book
from accounts.views import TokenDecoder


# Create your views here.
class CreatePublisher(APIView):
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
            return Response({'Message': 'There is no user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
            
        if not (admin_user_instance.is_staff or admin_user_instance.is_superuser):
            return Response({'Message': 'User is not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Editorial created in the base.'}, status=status.HTTP_201_CREATED)
        return Response({'Message': 'Error to create', 'Detail error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DetailPublisher(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, publisher_id):
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
            return Response({'Message': 'There is no user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            publisher_instance = Publisher.objects.get(id=publisher_id)
        except Publisher.DoesNotExist:
            return Response({'Message': 'There is no publisher associated with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)


        books_from_publisher = Book.objects.filter(editorial=publisher_instance.pk)
        if not books_from_publisher:
            return Response({'Message': 'No books from the respective publisher'}, status=status.HTTP_400_BAD_REQUEST)

        reviews_list = []
        books_list = []

        for book in books_from_publisher:
                
            reviews = Review.objects.filter(book=book.pk)
            for review in reviews:
                review_data = {
                        'id': review.pk,
                        'comment': review.comment,
                        'stars': review.stars,
                        'profile_id': review.user_creator.pk,
                        'book_id': review.book.pk
                        }
                reviews_list.append(review_data)
                
            book_data = {
                    'id': book.pk,
                    'title': book.title,
                    'subtitle': book.subtitle,
                    'isbn': book.isbn,
                    'author': book.author,
                    'publication_date': book.publication_date,
                    'synopsis': book.synopsis,
                    'gender': book.gender.name,
                    'reviews': reviews_list
                }
            books_list.append(book_data)
            
        editorial_data = {
                'name': publisher_instance.name,
                'books': books_list
                }
        return Response({'Publisher data': editorial_data}, status=status.HTTP_200_OK)
        

class DeletePublisher(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request, publisher_id):
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
            return Response({'Message': 'There is no user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            publisher_editorial = Publisher.objects.get(id=publisher_id)
        except Publisher.DoesNotExist:
            return Response({'Message': 'There is no publisher associated with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)

        if not (admin_user_instance.is_staff or admin_user_instance.is_superuser):
            return Response({'Message': 'User is not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

        publisher_editorial.delete()
        return Response({'Message': 'Publisher deleted'}, status=status.HTTP_200_OK)


class UpdatePublisher(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, publisher_id):
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
            return Response({'Message': 'There is no user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            publisher_editorial = Publisher.objects.get(id=publisher_id)
        except Publisher.DoesNotExist:
            return Response({'Message': 'There is no publisher associated with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not (admin_user_instance.is_staff or admin_user_instance.is_superuser):
            return Response({'Message': 'User is not an admin'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PublisherSerializer(instance=publisher_editorial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            publisher_editorial_data = {
                'id': publisher_editorial.pk,
                'name': publisher_editorial.name
            }
            return Response({'Message': 'Successfully updated the editorial', 'Data updated': publisher_editorial_data}, status=status.HTTP_200_OK)
        return Response({'Message': 'An error occurred while updating the publisher', 'Detail error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListBooksPublisher(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, publisher_id):
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
            return Response({'Message': 'There is no user associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            publisher_instance = Publisher.objects.get(id=publisher_id)
        except Publisher.DoesNotExist:
            return Response({'Message': 'There is no publisher associated with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)

        books_from_publisher = Book.objects.filter(editorial=publisher_instance.pk)
        if not books_from_publisher:
            return Response({'Message': 'No books from the respective publisher'}, status=status.HTTP_400_BAD_REQUEST)

        reviews_list = []
        books_list = []
        for book in books_from_publisher:
                
            reviews = Review.objects.filter(book=book.pk)
            for review in reviews:
                review_data = {
                    'id': review.pk,
                    'comment': review.comment,
                    'stars': review.stars,
                    'user_creator': review.user_creator.pk,
                    'book': review.book.pk
                    }
                reviews_list.append(review_data)
                
            book_data = {
                    'id': book.pk,
                    'title': book.title,
                    'subtitle': book.subtitle,
                    'isbn': book.isbn,
                    'author': book.author,
                    'publication_date': book.publication_date,
                    'synopsis': book.synopsis,
                    'gender': book.gender.name,
                    'reviews': reviews_list
                }
            books_list.append(book_data)
        return Response({'Message': 'List of books from publisher', 'Books': books_list}, status=status.HTTP_200_OK)