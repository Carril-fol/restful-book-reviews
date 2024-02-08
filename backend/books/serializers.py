import datetime
from django.utils import timezone

from rest_framework import serializers

from .models import *

# Create your serializers here.
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True}
        }
    
    def validate_gender(self, validate_data):
        gender = validate_data['name']
        if (len(gender)) > 0:
            raise serializers.ValidationError('The name of the gender must have more than one character.')
        elif (str(gender).isdigit()):
            raise serializers.ValidationError('Book genres cannot have numbers, only letters.')
        return gender
    

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': True},
            'subtitle' : {'required': False},
            'isbn': {'required': True},
            'author': {'required': True},
            'publication_date': {'required': True},
            'synopsis': {'required': True},
            'editorial': {'required': True},
            'gender': {'required': True}
        }
    
    def validate_title(self, validate_data):
        title = validate_data['title']
        if len(str(title)) > 1:
            raise serializers.ValidationError('The "title" must have more than one character.')
        return title


    def validate_sub_title(self, validate_data):
        subtitle = validate_data['subtitle']
        if len(str(subtitle)) > 1:
            raise serializers.ValidationError('The "subtitle" must have more than one character.')
        return subtitle

    def validate_isbn(self, validate_data):
        isbn = validate_data['isbn']
        if len(str(isbn)) < 13:
            raise serializers.ValidationError('The ISBN must be 13 characters long.')
        elif not (str(isbn).isdigit()):
            raise serializers.ValidationError(f'The ISBN must be only numbers.')
        return isbn

    def validate_author(self, validate_data):
        author = validate_data['author']
        if str(author).isdigit():
            raise serializers.ValidationError('The author must be only letters.')
        elif len(str(author)) < 1:
            raise serializers.ValidationError('The author must be longer than 1.')
        return author

    def validate_publication_date(self, validate_data):
        publication_date = validate_data['publication_date']
        data_format = timezone.datetime.date(publication_date)
        current_date = datetime.date.today()
        if data_format > current_date:
            raise serializers.ValidationError('The date must be current or less than the current date.')
        return publication_date

    def validate_synopsis(self, validate_data):
        synopsis = validate_data['synopsis']
        if (len(str(synopsis))) < 50:
            raise serializers.ValidationError('The "synopsis" must be longer than 50 characters.')
        return synopsis

    def validate_editorial(self, validate_data):
        editorial = validate_data['editorial']
        if not editorial:
            raise serializers.ValidationError('The "editorial" field is required.')
        elif not Editorial.objects.filter(name=editorial).exists():
            raise serializers.ValidationError('The "editorial" does not exist.')
        return editorial

    def validate_gender(self, validate_data):
        gender = validate_data['gender']
        if not gender:
            raise serializers.ValidationError('The "gender" field is required.')
        elif not Gender.objects.filter(name=gender).exists():
            raise serializers.ValidationError('The "Gender" does not exist.')
        return gender