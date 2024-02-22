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
    
    def validate_gender(self, validate_data):
        gender = validate_data['name']
        if (len(gender)) > 0:
            raise serializers.ValidationError('The name of the gender must have more than one character.')
        elif (str(gender).isdigit()):
            raise serializers.ValidationError('Book genres cannot have numbers, only letters.')
        return gender