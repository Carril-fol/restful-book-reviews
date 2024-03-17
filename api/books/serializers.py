from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from genders.models import Gender
from .models import *

# Create your serializers here.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'title': {'required': False},
            'subtitle' : {'required': False},
            'isbn': {'required': False},
            'image_book': {'required': False},
            'author': {'required': False},
            'publication_date': {'required': False},
            'synopsis': {'required': False},
            'editorial': {'required': False},
            'gender': {'required': False}
        }
    
    def validate_title(self, validate_data):
        validate_data = str(self.initial_data['title'])
        if len(str(validate_data)) <= 1:
            raise ValidationError('The "title" must have more than one character.')
        return validate_data

    def validate_sub_title(self, validate_data):
        validate_data = self.initial_data['subtitle']
        if len(str(validate_data)) <= 1:
            raise ValidationError('The "subtitle" must have more than one character.')
        return validate_data

    def validate_isbn(self, validate_data):
        validate_data = str(self.initial_data['isbn'])
        if len(validate_data) < 13:
            raise ValidationError('The ISBN must be 13 characters long.')
        elif not (validate_data.isdigit()):
            raise ValidationError(f'The ISBN must be only numbers.')
        return validate_data

    def validate_author(self, validate_data):
        validate_data = str(self.initial_data['author'])
        if str(validate_data).isdigit():
            raise ValidationError('The author must be only letters.')
        elif len(str(validate_data)) <= 1:
            raise ValidationError('The author must be longer than 1.')
        return validate_data

    def validate_publication_date(self, validate_data):
        validate_data_str = self.initial_data['publication_date']
        if validate_data_str:
            validate_data = datetime.strptime(validate_data_str, '%Y-%m-%d').date()
            current_date = datetime.today().date()
            if validate_data > current_date:
                raise ValidationError('The date must be current or less than the current date.')
        return validate_data

    def validate_synopsis(self, validate_data):
        validate_data = str(self.initial_data['synopsis'])
        if (len(validate_data)) < 30:
            raise ValidationError('The "synopsis" must be longer than 50 characters.')
        return validate_data

    def validate_gender(self, validate_data):
        if not validate_data:
            raise ValidationError('The "gender" field is required.')
        gender = Gender.objects.get(id=int(self.initial_data['gender']))
        if not gender:
            raise ValidationError('Gender not found.')
        return validate_data