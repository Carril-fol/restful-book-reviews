from rest_framework import serializers
from rest_framework.serializers import ValidationError

from profiles.models import Profile
from books.models import Book

from .models import Review

# Create your serializers here.
class ReviewSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False)
    stars = serializers.IntegerField(required=True)
    profile_creator = serializers.IntegerField(required=True)
    book_id = serializers.IntegerField(required=True)

    def validate_comment(self, validate_data):
        comment = self.initial_data['comment']
        if len(comment) <= 1:
            raise ValidationError('the comment has to have more than one character.')
        return validate_data
    
    def validate_stars(self, validate_data):
        stars = int(self.initial_data['stars'])
        if stars < 0:
            raise ValidationError('The stars has to be more than 0.')
        elif stars > 5:
            raise ValidationError('the stars cannot be more than 5.')
        return validate_data
    
    def validate_profile_creator(self, validate_data):
        profile_id = int(self.initial_data['profile_creator'])
        if profile_id <= 1:
            raise ValidationError('IDs from users start in 1, no from 0.')
        profile_data = Profile.objects.get(id=profile_id)
        if profile_data:
            return profile_data
        raise ValidationError('That ID not exists in profiles.')
    
    def validate_book(self, validate_data):
        book_id = int(self.initial_data['book_id'])
        if book_id <= 1:
            raise ValidationError('IDs from books start in 1, no from 0.')
        book = Book.objects.get(id=book_id)
        if book:
            return book
        raise ValidationError('That ID not exists in books.')
    
    def create(self, clean_data):
        profile_id = self.validate_profile_creator(clean_data)
        book_id = self.validate_book(clean_data)
        review = Review.objects.create(
            comment=clean_data['comment'],
            stars=clean_data['stars'],
            profile_creator=profile_id,
            book=book_id
        )
        review.save()
        return review
    
    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.profile_creator = self.validate_profile_creator(validated_data.get('profile_creator', instance.profile_creator))
        instance.book = self.validate_book(validated_data.get('book_id', instance.book.id))
        instance.save()
        return instance