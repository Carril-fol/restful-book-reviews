import requests
import os

from django.db import models

from accounts.models import UserCustom
from .utils import profile_pictures_per_user_directory

# Create your models here.
class Profile(models.Model):
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    img_profile = models.ImageField(upload_to=profile_pictures_per_user_directory, null=True, blank=True)
    followers = models.ManyToManyField(UserCustom, related_name='following', blank=True)
    user = models.ForeignKey(UserCustom, on_delete=models.CASCADE, null=False, blank=False)

    def default_image(self):
        default_img_profile_path = 'media/images/profiles/default_user_icon.webp'
        default_img_set = None
        if not os.path.exists(default_img_profile_path):
            os.makedirs(os.path.dirname(default_img_profile_path), exist_ok=True)
            default_img_profile = 'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/271deea8-e28c-41a3-aaf5-2913f5f48be6/de7834s-6515bd40-8b2c-4dc6-a843-5ac1a95a8b55.jpg/v1/fill/w_300,h_300,q_75,strp/default_user_icon_4_by_karmaanddestiny_de7834s-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9MzAwIiwicGF0aCI6IlwvZlwvMjcxZGVlYTgtZTI4Yy00MWEzLWFhZjUtMjkxM2Y1ZjQ4YmU2XC9kZTc4MzRzLTY1MTViZDQwLThiMmMtNGRjNi1hODQzLTVhYzFhOTVhOGI1NS5qcGciLCJ3aWR0aCI6Ijw9MzAwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.W7L0Rf_YqFzX9yxDfKtIMFnnRFdjwCHxi7xeIISAHNM'
            response = requests.get(default_img_profile)
            if response.status_code == 200:
                with open(default_img_profile_path, 'wb') as f:
                    f.write(response.content)
        return default_img_profile_path

    def save(self, *args, **kwargs):
        if not self.img_profile:
            default_image_set = self.default_image()
            self.img_profile = default_image_set
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} / ID: {self.user.pk}'