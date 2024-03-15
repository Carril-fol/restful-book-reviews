from django.db import models
from django.core.exceptions import ValidationError

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