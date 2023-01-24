from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    ''' Serializer for registering a user'''
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

class UserLoginSerializer(serializers.ModelSerializer):
    ''' Serializer for logging in a user'''
    class Meta:
        model = User
        fields = ('email', 'password')