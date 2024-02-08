from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Editorial(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def save(self, *args, **kwargs):
        existing_name = Editorial.objects.filter(name=self.name).first()
        if existing_name:
            raise ValidationError(f'The editorial: "{self.name}" is already in the database.')
        super(Editorial, self).save(*args, **kwargs)

    def __str__(self):
        return f'Editorial: {self.name}'