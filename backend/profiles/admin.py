from django.contrib import admin

from .models import Domicile, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Domicile)