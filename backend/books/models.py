from django.db import models
from django.core.exceptions import ValidationError

from publishers.models import Editorial

# Create your models here.
class Gender(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    synopsis = models.TextField()

    def save(self, *args, **kwargs):
        existing_gender = Gender.objects.filter(name=self.name).first()
        if existing_gender:
            raise ValidationError(f'The gender: "{self.name}" is already in the database/')
        super(Gender, self).save(*args, **kwargs)

    def __str__(self):
        return f'Gender: {self.name}'


class Book(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=False, blank=False)
    author = models.CharField(max_length=255, null=False, blank=False)
    publication_date = models.DateField()
    synopsis = models.TextField()
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, null=False, blank=False)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=False, blank=False)

    def save(self, *args, **kwargs):
        existing_book = Book.objects.filter(isbn=self.isbn).first()
        if existing_book:
            raise ValidationError(f'The ISBN: "{self.isbn}" is already in the database.')
        if (len(self.isbn)) < 13:
            raise ValidationError(f'The ISBN: "{self.isbn}" must have a length of 13.')
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f'ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Editorial: {self.editorial}, Gender: {self.gender}'