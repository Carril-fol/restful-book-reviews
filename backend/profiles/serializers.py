from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Profile

# Create your serializers here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'img_profile': {'required': False},
            'user': {'required': True}
        }

    def validate_first_name(self, validate_data):
        validate_data = str(self.initial_data['first_name'])
        if len(validate_data) <= 1:
            raise ValidationError('The name cannot be incomplete')
        return (validate_data.capitalize())

    def validate_last_name(self, validate_data):
        validate_data = str(self.initial_data['last_name'])
        if len(validate_data) <= 1:
            raise ValidationError('The last name cannot be incomplete.')
        return (validate_data.capitalize())