from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from .models import UserCustom
from profiles.models import Profile

# Create your serializers here.
class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=UserCustom.objects.all())]
    )
    first_name = serializers.CharField(
        required=True
    )
    last_name = serializers.CharField(
        required=True
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserCustom.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        required=True,
        write_only=True
    )

    def validate_email(self, validated_data):
        if '@' not in self.initial_data['email']:
            raise ValidationError('It is not an email. Please enter again')
        return validated_data

    def validate_confirm_password(self, validate_data):
        if self.initial_data['password'] != self.initial_data['confirm_password']:
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
        self.validate_email(validated_data)
        self.validate_character_lower_in_password(validated_data)
        self.validate_character_upper_in_password(validated_data)
        self.validate_length_password(validated_data)
        self.validate_number_in_password(validated_data)
        self.validate_security_password(validated_data)
        return validated_data

    def create(self, clean_data):
        user = UserCustom.objects.create(
            username=clean_data['username'],
            first_name=clean_data['first_name'],
            last_name=clean_data['last_name'],
            email=clean_data['email']
        )
        profile = Profile.objects.create(
            user=user
        )
        user.set_password(clean_data['confirm_password'])
        profile.save()
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True
    )
    password = serializers.CharField(
        required=True,
        write_only=True
    )
    
    def check_user_exists(self, clean_data):
        try:
            user = UserCustom.objects.get(email=clean_data['email'])
            return user
        except ObjectDoesNotExist:
            raise ValidationError('User not found')
    
    def check_user_verified(self, clean_data):
        user = UserCustom.objects.get(email=clean_data['email'])
        if not user.is_verified:
            raise ValidationError('User is not verified')
        return True
    
    def user_data(self, clean_data):
        user = UserCustom.objects.get(email=clean_data['email'])
        if not user:
            raise ValidationError('User not found')
        return user

    def check(self, clean_data):
        self.check_user_exists(clean_data)
        self.check_user_verified(clean_data)
        return clean_data