from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    """
    ModelSerializer class to represent registration.
    """
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password',
        )


class CustomTokenObtainPair(TokenObtainPairSerializer):
    """
    TokenObtainPairSerializer class to represent getting token registration.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        code = self.context['request'].data.get('verification_code')
        if code:
            attrs['password'] = code
            return super().validate(attrs)
        return 'verification_code is required.'


class UsersSerializer(serializers.ModelSerializer):
    """
    ModelSerializer class to represent CustomUser.
    """
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role',
        )
