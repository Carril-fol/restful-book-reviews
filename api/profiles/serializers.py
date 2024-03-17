from rest_framework import serializers
from rest_framework.serializers import ValidationError

from accounts.models import UserCustom

from .models import Profile

# Create your serializers here.
class UpdateProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    bio = serializers.CharField()
    location = serializers.CharField()
    img_profile = serializers.ImageField(required=False)
    extra_kwargs = {
        'first_name': {'required': False},
        'last_name': {'required': False},
        'img_profile': {'required': False}
    }

    def validate_username(self, validate_data):
        validate_data = str(self.initial_data['username'])
        if len(validate_data) <= 1:
            raise ValidationError('The username cannot be incomplete')
        return validate_data

    def validate_first_name(self, validate_data):
        validate_data = str(self.initial_data['first_name'])
        if len(validate_data) <= 1:
            raise ValidationError('The name cannot be incomplete')
        return validate_data

    def validate_last_name(self, validate_data):
        validate_data = str(self.initial_data['last_name'])
        if len(validate_data) <= 1:
            raise ValidationError('The last name cannot be incomplete.')
        return validate_data
    
    def update_user_data(self, profile_id):
        new_username = str(self.initial_data['username'])
        new_first_name = str(self.initial_data['first_name'])
        new_last_name = str(self.initial_data['last_name'])

        profile_data = Profile.objects.get(id=profile_id)
        user_data = UserCustom.objects.get(id=profile_data.user.pk)
        
        user_data.username = new_username
        user_data.first_name = new_first_name
        user_data.last_name = new_last_name
        user_data.save()
        return user_data
    
    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.img_profile = validated_data.get('img_profile', instance.img_profile)
        instance.save()
        self.update_user_data(instance.id)
        return instance