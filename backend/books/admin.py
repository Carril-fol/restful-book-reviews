from django.contrib import admin

from .models import Editorial, Gender, Book

# Register your models here.
admin.site.register(Editorial)
admin.site.register(Gender)
admin.site.register(Book)