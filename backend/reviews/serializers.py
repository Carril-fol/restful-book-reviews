from rest_framework import serializers

from books.models import Book

from .models import Review

# Create your serializers here.
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'comment': {'required': False},
            'stars': {'required': True},
            'likes': {'required': False},
            'user_creator': {'required': True},
            'book': {'required': True}
        }