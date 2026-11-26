from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Validate registration data and create a user."""

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )
    confirmed_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']

    def validate(self, attrs):
        """Validate password confirmation and strength."""
        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError({
                'confirmed_password': 'Passwords do not match.'
            })
        user = User(
            username=attrs['username'],
            email=attrs['email']
        )
        validate_password(attrs['password'], user)
        return attrs

    def create(self, validated_data):
        """Create a user with a securely hashed password."""
        validated_data.pop('confirmed_password')
        return User.objects.create_user(**validated_data)
