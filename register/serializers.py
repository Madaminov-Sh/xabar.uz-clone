from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from register.models import User, Profile, SocialNetwork, VerificationCode


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'confirm_password')

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data.update(instance.token())
        return data


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        authentication_kwargs = {
            self.username_field: email,
            'password': password
        }
        user = authenticate(**authentication_kwargs)
        # checked_password = check_password(password, user.password)

        if user:
            self.user = user
        else:
            raise AuthenticationFailed("User does not found")

        hashed_password = make_password(password)
        refresh = self.get_token(user)
        attrs['password'] = hashed_password
        attrs['access'] = str(refresh.access_token)
        attrs['refresh'] = str(refresh)

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email', None)

        if not email:
            raise ValidationError({"success": False, "message": "email is required."})

        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError({"success": False, "message": "email not found."})

        attrs['user'] = user.first()
        return attrs


class SocialNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetwork
        fields = ('id', 'title', 'url')


class ProfileSerializer(serializers.ModelSerializer):
    social_network = SocialNetworkSerializer(read_only=True)
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'full_name', 'user', 'image',
                  'big_description', 'small_description', 'email',
                  'job_title', 'created_at', 'updated_at', 'social_network')

        extra_kwargs = {
            'full_name': {'required': False},
            'email': {'required': False}
        }


