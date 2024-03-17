from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import isVerified
from books.models import Book

from .permissions import hisReview
from .models import Review
from .serializers import ReviewSerializer

# Create your views here.
class PublishReview(APIView):
    """
    Example:

    POST: api/publish-review/<int:book_id>/

    ```
    Aplication data:
    {
        'comment': 'Text for the review',
        'stars': 'Califications for the book',
        'profile_creator': 'ID from the profile creator review',
        'book_id': 'ID from book'
    }

    Successful response (code 200 - OK):
    {
        "Message": "Review successfully published."
    }
    
    Response with validation errors (code 400 - Bad Requests):
    {
        "Error": {
            'comment': ['the comment has to have more than one character...'],
            'stars': ['The stars has to be more than 0...']
            // Other errors of validation from the serializer.
        }
    }
    ```
    """
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def post(self, request, book_id):
        try:
            book_instance = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'Message': 'No book is associated with the entered ID.'}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Review successfully published.'}, status=status.HTTP_201_CREATED)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class DeleteReview(APIView):
    """
    Example:

    DELETE: api/delete-review/<int:review_id>/

    ```
    Successful response (code 200 - OK):
    {
        "Message": "Review successfully deleted."
    }
    
    Response with validation errors (code 400 - Bad Requests):
    {
        "Message": "There is no review associated with the ID entered."
    }
    ```
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified, hisReview]

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'Message': 'There is no review associated with the ID entered.'}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({'Message': 'Review successfully deleted.'}, status=status.HTTP_200_OK)


class UpdateReview(APIView):
    """
    Example:

    PUT: api/update-review/<int:review_id>/

    ```
    Aplication data:
    {
        'comment': ' New text for comment in the review',
        'stars': 'New calification for the book',
        'profile_creator': 'ID from the profile creator review',
        'book_id': 'ID from book'
    }

    Successful response (code 200 - OK):
    {
        "Message": "Successfully updated the review."
    }
    
    Response with validation errors (code 400 - Bad Requests):
    {
        "Error": {
            'comment': ['the comment has to have more than one character...'],
            'stars': ['The stars has to be more than 0...']
            // Other errors of validation from the serializer.
        }
    }
    ```
    """
    serializer_class = ReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified, hisReview]

    def put(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'Message': 'The ID entered does not belong to any review.'}, status=status.HTTP_404_NOT_FOUND)
        data=request.data
        serializer = self.serializer_class(instance=review, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Successfully updated the review.'}, status=status.HTTP_200_OK)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ListReviewsBookSpecific(APIView):
    """
    Example:

    GET: api/reviews/book/<int:book_id>/

    ```
    Successful response (code 200 - OK):
    {
        "Reviews": [
            'id': review.pk,
            'comment': review.comment,
            'stars': review.stars,
            'likes': review.likes_count(),
            'profile_creator': review.profile_creator.pk,
            'book': review.book.pk
        ]
    }
    
    Response with validation errors (code 404 - Not found):
    {
        'Message': 'There is no record of a book with the ID entered.'
    }
    ```
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request, book_id):
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
                'profile_creator': review.profile_creator.pk,
                'book': review.book.pk
            }
            list_reviews.append(review_data)
        return Response({'Reviews': list_reviews}, status=status.HTTP_200_OK)


class DetailReview(APIView):
    """
    Example:

    GET: api/detail/review/<int:review_id>/

    ```
    Successful response (code 200 - OK):
    {
        'Review detail': {
            'id': review.pk,
            'comment': review.comment,
            'stars': review.stars,
            'likes': review.likes_count(),
            'profile_creator': review.profile_creator.pk,
            'book': review.book.pk
        }
    }

    Response with validation errors (code 404 - Not found):
    {
        'Message': 'There is no record of a book with the ID entered.'
    }
    ```
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'Message': 'There is no review with this ID entered.'}, status=status.HTTP_404_NOT_FOUND)
        review_data = {
            'id': review.pk,
            'comment': review.comment,
            'stars': review.stars,
            'likes': review.likes_count(),
            'profile_creator': review.profile_creator.pk,
            'book': review.book.pk
        }
        return Response({'Review detail': review_data}, status=status.HTTP_200_OK)