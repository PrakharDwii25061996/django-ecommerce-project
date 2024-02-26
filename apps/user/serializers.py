from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from django.core.exceptions import ValidationError
from django.contrib.auth import login, authenticate, get_user_model, get_user
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import CustomUser, Profile


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'uuid', 'id', 'email', 'first_name',
            'last_name', 'password', 'mobile_number',
            'permanent_address', 'residential_address',
            'created_at', 'last_modified'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if not data.get('email'):
            raise serializers.ValidationError("Please enter email.")
        else:
            email = data.get('email')
            user = CustomUser.objects.filter(email=email)
            if user.exists():
                return serializers,ValidationError("Email already exists.")

        if not data.get('password'):
            return serializers.ValidationError("Please enter password")
        return data

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            mobile_number=validated_data.get('mobile_number'),
            permanent_address=validated_data.get('permanent_address'),
            residential_address=validated_data.get('residential_address')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user and user.is_active:
            return user
        raise serializers.ValidationError('Invalid credentials')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')

        user = CustomUser.objects.filter(email=email).first()

        if (user is not None) and user.is_active:
            return user
        raise serializers.ValidationError('User does not exists.')


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=55)
    confirm_password = serializers.CharField(max_length=55)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not (confirm_password and password):
            raise serializers.ValidationError('Password is invalid.')
        elif confirm_password != password:
            raise serializers.ValidationError('Password does not match')
        return data


class ProfileEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

    def validate_image(self, data):
        image_name = data._name

        if image_name.split('.')[-1] not in ['jpeg', 'jpg', 'png']:
            raise serializers.ValidationError('Image Uploaded in incorrect format')

        return data

    def update(self, instance, validated_data):

        if validated_data.get('image'):
            instance.image = validated_data.get('image')

        instance.alternate_number = validated_data.get(
            'alternate_number',
            instance.alternate_number
        )
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.postal_code = validated_data.get(
            'postal_code', instance.postal_code
        )
        instance.latitude = validated_data.get(
            'latitude', instance.latitude
        )
        instance.longitude = validated_data.get(
            'longitude', instance.longitude
        )
        instance.save()
        return instance
