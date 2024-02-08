from rest_framework import serializers

from .models import *

# Create your serializers here.
class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True}
        }

    def validate_name(self, validate_data):
        name_editorial = validate_data['name']
        if (len(name_editorial)) < 1:
            raise serializers.ValidationError('The "name of the publisher" must have more than one character.')
        elif (str(name_editorial).isdigit()):
            raise serializers.ValidationError("Publisher's name cannot have numbers, only letters.")
        return name_editorial