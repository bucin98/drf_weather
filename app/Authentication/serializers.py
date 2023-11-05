from rest_framework import serializers
from .models import CustomUser


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('location',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'location')
        extra_kwargs = {
            'password': {'write_only': True},
            'location': {'required': False}
        }

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            location=validated_data.get('location')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
