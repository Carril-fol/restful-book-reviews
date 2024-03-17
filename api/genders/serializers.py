from rest_framework import serializers

from .models import *

# Create your serializers here.
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['name', 'synopsis']
        extra_kwargs = {
            'name': {'required': True},
            'synopsis' : {'required': True}
        }
    
    def validate_name(self, validate_data):
        validate_data = self.initial_data['name']
        if (len(validate_data)) <= 1:
            raise serializers.ValidationError('The name of the gender must have more than one character.')
        elif (str(validate_data).isdigit()):
            raise serializers.ValidationError('Book genres cannot have numbers, only letters.')
        return validate_data

    def validate_synopsis(self, validate_data):
        validate_data = self.initial_data['synopsis']
        if (len(validate_data)) < 50:
            raise serializers.ValidationError('The synopsis of the gender must have more than 50 character.')
        return validate_data

    def validate_gender(self, validate_data):
        validate_data = self.initial_data['gender']
        if (len(validate_data)) <= 1:
            raise serializers.ValidationError('The name of the gender must have more than one character.')
        elif (str(validate_data).isdigit()):
            raise serializers.ValidationError('Book genres cannot have numbers, only letters.')
        return validate_data