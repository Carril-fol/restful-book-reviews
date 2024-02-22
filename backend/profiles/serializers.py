from rest_framework import serializers

from .models import Profile

# Create your serializers here.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'dni': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'img_profile': {'required': False}
        }

    def validate_dni(self, validate_data):
        dni = validate_data['dni']
        if str(dni).is_digit():
            if len(dni) < 8:
                raise serializers.ValidationError('The DNI cannot be less than 8 characters long.')
            return validate_data
        raise serializers.ValidationError('The DNI must contain only numerical characters.')

    def validate_first_name(self, validate_data):
        first_name = validate_data['first_name']
        if len(first_name) <= 1:
            raise serializers.ValidationError('The name cannot be incomplete')
        return validate_data

    def validate_last_name(self, validate_data):
        last_name = validate_data['last_name']
        if len(last_name) <= 1:
            raise serializers.ValidationError('The last name cannot be incomplete.')
        return validate_data

    def save(self, **kwargs):
        user_id = kwargs.pop('user_id', None)
        instance = super().save(**kwargs)
        if user_id is not None:
            instance.user_id = user_id
            instance.save()
        return instance