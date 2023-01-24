from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.contrib.auth import get_user_model
from api.serializers import *


class UserRegisterViewSet(ViewSet):
    ''' View for registering a user'''
    
    user_model = get_user_model()

    def register(self, request):
        ''' PUT: /api/auth/register/'''
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.data['email'] = serializer.data['email'].lower()
        if self.user_model.objects.filter(email=serializer.data['email']).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = self.user_model.objects.create_user(**serializer.data)
        user.is_active = True
        user.save()
        return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)




        
