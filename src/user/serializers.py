from .models import CustomUser

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'mobile_number')
        extra_kwargs = {'password': {'write_only': True}}