from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

from profiles.models import Profile
from books.models import Book

# Create your models here.
class Review(models.Model):
    comment = models.TextField()
    stars = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='likes_reviews', blank=True)
    user_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=False, blank=False)

    def clean(self):
        if self.stars < 1 or self.stars > 5:
            raise ValidationError("Stars must be between 1 and 5.")
        return self.stars
    
    def likes_count(self):
        counts_likes = self.likes.count()
        return counts_likes
    
    def __str__(self):
        count_likes = self.likes_count()
        return f'User: {self.user_creator}, Comment: {self.comment}, Likes review: {count_likes}, Stars: {self.stars}'