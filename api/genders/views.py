from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.permissions import isAdminCustom, isVerified
from books.models import Book

from .models import Gender
from .serializers import GenderSerializer

# Create your views here.
class GenderCreate(APIView):
    serializer_class = GenderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdminCustom]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'Gender created.'}, status=status.HTTP_201_CREATED)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GenderDetail(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request, gender_id):
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
            'id': gender.pk,
            'gender': gender.name,
            'synopsis': gender.synopsis
        }
        return Response({'Gender data': gender_data, 'Books with that gender': books_list}, status=status.HTTP_200_OK)


class GenderList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [isVerified]

    def get(self, request):
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
    permission_classes = [isAdminCustom]

    def delete(self, request, gender_id):
        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({'Error': 'There is no gender introduced'}, status=status.HTTP_404_NOT_FOUND)
        gender.delete()
        return Response({'Message': 'The entered gender is deleted.'}, status=status.HTTP_200_OK)


class GenderUpdate(APIView):
    serializer_class = GenderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [isAdminCustom]

    def put(self, request, gender_id):
        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({'Error': 'There is no gender introduced'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = self.serializer_class(instance=gender, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'The entered gender has been updated.'}, status=status.HTTP_200_OK)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
