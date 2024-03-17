import os
import requests

from django.db import models

from genders.models import Gender
from .utils import book_pictures

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=False, blank=False)
    image_book = models.ImageField(upload_to=book_pictures, null=True, blank=True)
    author = models.CharField(max_length=255, null=False, blank=False)
    publication_date = models.DateField()
    synopsis = models.TextField()
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=False, blank=False)

    def default_img(self):
        default_img_path = 'media/images/books/no_image_available.webp'
        default_img_set = None
        if not os.path.exists(default_img_path):
            os.makedirs(os.path.dirname(default_img_path), exist_ok=True)
            default_img = 'https://demofree.sirv.com/nope-not-here.jpg'
            response = requests.get(default_img)
            if response.status_code == 200:
                with open(default_img_path, 'wb') as f:
                    f.write(response.content)
        return default_img_path

    def save(self, *args, **kwargs):
        if not self.image_book:
            default_image_set = self.default_img()
            self.image_book = default_image_set
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f'ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Gender: {self.gender}'