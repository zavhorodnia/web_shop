from .models import ShopUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ['id', 'email', 'type', 'shops']

    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return "ADMIN" if obj.is_admin else "USER"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserRegistrationSerializer, self).create(validated_data)
