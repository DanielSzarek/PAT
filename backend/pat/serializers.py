from .models import User, Pack
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'type')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserPasswordSerializer(serializers.ModelSerializer):
    """
    Serializer for password change endpoint.
    """
    class Meta:
        model = User

        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)


class PackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack
        exclude = ['add_date']
