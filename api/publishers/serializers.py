from rest_framework import serializers

from .models import *

# Create your serializers here.
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name']
        extra_kwargs = {
            'name': {'required': True}
        }