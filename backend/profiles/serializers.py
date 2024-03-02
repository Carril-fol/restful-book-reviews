from rest_framework import serializers

from .models import Profile

# Create your serializers here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'img_profile': {'required': False}
        }

    def validate_first_name(self, validate_data):
        if len(str(self.initial_data['first_name'])) <= 1:
            raise serializers.ValidationError('The name cannot be incomplete')
        return validate_data

    def validate_last_name(self, validate_data):
        if len(str(self.initial_data['last_name'])) <= 1:
            raise serializers.ValidationError('The last name cannot be incomplete.')
        return validate_data
