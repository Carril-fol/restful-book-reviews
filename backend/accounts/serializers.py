from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from profiles.models import Profile

# Create your serializers here.
class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=False
    )
    last_name = serializers.CharField(
        required=False
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']
        extra_kwargs = {
            'password' : {'required': True},
            'password2' : {'required': True},
            'username' : {'required' : True},
            'first_name' : {'required' : False},
            'last_name' : {'required' : False},
            'email' : {'required' : True}
        }

    def validate_email(self, validated_data):
        if '@' not in validated_data:
            raise serializers.ValidationError('It is not an email. Please enter again')
        return validated_data
    
    def validate_password2(self, validated_data):
        if self.initial_data['password'] != validated_data:
            raise serializers.ValidationError('Passwords don`t match')
        return validated_data

    def create(self, validated_data):
        user_to_create = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )
        profile_to_create = Profile.objects.create(
            user=user_to_create
        )
        user_to_create.set_password(validated_data['password2'])
        user_to_create.save()
        profile_to_create.save()
        return user_to_create