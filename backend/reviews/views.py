from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.views import TokenDecoder
from books.models import Book

from .models import Review
from .serializers import ReviewSerializer


# Create your views here.
class PublishReview(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request, book_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            book_instace = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'No book is associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user_instance = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'Message': 'The ID entered does not belong to any user.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Review successfully published.'}, status=status.HTTP_201_CREATED)
        return Response({'Message': 'An error occurred while publishing the review.', 'Detail error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteReview(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request, review_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'Message': 'There is no review associated with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)
        
        if review.user_creator.pk != user_id:
            return Response({'Error': 'You do not have permission to delete this review.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        review.delete()
        return Response({'Message': 'Review successfully deleted.'}, status=status.HTTP_200_OK)


class UpdateReview(APIView):
    authentication_classes = [JWTAuthentication]

    def put(self, request, review_id):
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
            return Response({'Message': 'The ID entered does not belong to any user.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'Message': 'The ID entered does not belong to any review.'}, status=status.HTTP_404_NOT_FOUND)

        if review.user_creator.pk != user_id:
            return Response({'Error': 'You do not have permission to delete this review.'}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ReviewSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Successfully updated the review.'}, status=status.HTTP_200_OK)
        return Response({'Message': 'An error occurred while publishing the review', 'Detail error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListReviewsBookSpecific(APIView):
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
            book_instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'There is no record of a book with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(book=book_instance)
        list_reviews = []
        for review in reviews:
            review_data = {
                'id': review.pk,
                'comment': review.comment,
                'stars': review.stars,
                'likes': review.likes_count(),
                'author_review': review.user_creator.pk,
                'book': review.book.pk
            }
            list_reviews.append(review_data)
        return Response({'Reviews': list_reviews}, status=status.HTTP_200_OK)


class DetailReview(APIView):

    def get(self, request, review_id):
        token_decoder = TokenDecoder()
        raw_token = request.COOKIES.get('refresh')
        if not raw_token:
            return Response({'Error': 'Token is not found in cookies.' }, status=status.HTTP_401_UNAUTHORIZED)
        user_id = token_decoder.decode_token(raw_token)
        if user_id is None:
            return Response({'Error': 'Token expired or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'Message': 'There is no review with this ID entered.'}, status=status.HTTP_404_NOT_FOUND)
            
        review_data = {
            'id': review.pk,
            'comment': review.comment,
            'stars': review.stars,
            'likes': review.likes_count(),
            'author_review': review.user_creator.pk,
            'book': review.book.pk
        }
        return Response({'Review detail': review_data}, status=status.HTTP_200_OK)