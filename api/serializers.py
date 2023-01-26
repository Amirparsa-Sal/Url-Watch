from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Url, Warning

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    ''' Serializer for registering a user'''
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

class UrlSerializer(serializers.ModelSerializer):
    ''' Serializer for adding urls'''
    class Meta:
        model = Url
        read_only_fields = ('id', 'created_at', 'updated_at', 'failed_times')
        fields = read_only_fields + ('url', 'threshold')

class UrlCompactSerializer(serializers.ModelSerializer):
    ''' Serializer for showing a list of urls'''
    class Meta:
        model = Url
        fields = ('id', 'url')

class WarningSerializer(serializers.ModelSerializer):
    ''' Serializer for showing a list of warnings'''
    class Meta:
        model = Warning
        fields = ('id', 'created_at', 'result_code')
        