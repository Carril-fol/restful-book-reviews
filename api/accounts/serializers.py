from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from profiles.models import Profile

# Create your serializers here.
class UserRegisterSerializer(serializers.ModelSerializer):
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

    def validate_email(self, validate_data):
        validate_data = str(self.initial_data['email'])
        if '@' not in validate_data:
            raise ValidationError('The email is not valid.')
        return validate_data

    def validate_length_username(self, validate_data):
        validate_data = str(self.initial_data['username'])
        if len(validate_data) < 3:
            raise ValidationError('Username length should be at least 3')
        elif len(validate_data) > 8:
            raise ValidationError('Username length should be not be greater than 8')
        return validate_data

    def validate_email(self, validated_data):
        if '@' not in validated_data:
            raise ValidationError('It is not an email. Please enter again')
        return validated_data

    def validate_confirm_password(self, validate_data):
        if self.initial_data['password'] != validate_data:
            raise ValidationError('Passwords don`t match')
        return validate_data
    
    def validate_length_password(self, validate_data):
        confirm_password = self.initial_data['confirm_password']
        if len(str(confirm_password)) < 6:
            raise ValidationError('Password length should be at least 6')
        elif len(str(confirm_password)) > 20:
            raise ValidationError('Password length should be not be greater than 8')
        return validate_data

    def validate_security_password(self, validate_data):
        signal_allowed_found = False
        allowed_signals = ['-', '_', '@', '#', '$', '%', '&', '*', '!', '¡', '¿', '?', '=']
        validate_data = (str(self.initial_data['confirm_password']))
        while signal_allowed_found == False:
            for char in validate_data:
                if char in allowed_signals:
                    signal_allowed_found = True
                    return validate_data
            if not signal_allowed_found:
                raise ValidationError('Password should have at least one of the symbols $,@,#,-,_,=,%,&,*,!,¡,¿,?,=')
        return validate_data
    
    def validate_number_in_password(self, validate_data):
        validate_data = str(self.initial_data['confirm_password'])
        if not any(char.isdigit() for char in validate_data):
            raise ValidationError('Password should have at least one numeral')
        return validate_data
    
    def validate_character_upper_in_password(self, validate_data):
        validate_data = str(self.initial_data['confirm_password'])
        if not any(char.isupper() for char in validate_data):
            raise ValidationError('Password should have at least one uppercase letter')
        return validate_data
    
    def validate_character_lower_in_password(self, validate_data):
        validate_data = str(self.initial_data['confirm_password'])
        if not any(char.islower() for char in validate_data):
            raise ValidationError('Password should have at least one lowercase letter')
        return validate_data

    def check(self, validated_data):
        self.validate_length_username(validated_data)
        self.validate_email(validated_data)
        self.validate_character_lower_in_password(validated_data)
        self.validate_character_upper_in_password(validated_data)
        self.validate_length_password(validated_data)
        self.validate_number_in_password(validated_data)
        self.validate_security_password(validated_data)
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
    
    def user_data(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('User not found')
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True
    )
    password = serializers.CharField(
        required=True,
        write_only=True
    )
    
    def check_user_exists(self, clean_data):
        username = clean_data['username']
        password = clean_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError('User not found')
        return user