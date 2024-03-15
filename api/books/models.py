from django.db import models

from publishers.models import Publisher
from genders.models import Gender

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    publication_date = models.DateField()
    synopsis = models.TextField()
    editorial = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=False, blank=False)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f'ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Editorial: {self.editorial}, Gender: {self.gender}'