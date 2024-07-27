from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import IntegrityError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for the User model.
    Defines the fields to be serialized/deserialized.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'bio', 'profile_picture')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name',
                  'mobile_number', 'role', 'bio', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                mobile_number=validated_data['mobile_number'],
                role=validated_data['role'],
                bio=validated_data.get('bio', ''),
                profile_picture=validated_data.get('profile_picture', None)
            )
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({'error': str(e)})
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")
