from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.contrib.auth import get_user_model
from api.serializers import *


class UserRegisterViewSet(ViewSet):
    '''A view for registering a user using email, first_name, last_name, and password'''    
    user_model = get_user_model()

    def register(self, request):
        ''' POST: /api/auth/register/ '''
        serializer = UserRegisterSerializer(data=request.data)
        # Check if the user input is valid
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # make the email lowercase
        serializer.data['email'] = serializer.data['email'].lower()
        # check if a user with the same email already exists
        if self.user_model.objects.filter(email=serializer.data['email']).exists():
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # create the user
        user = self.user_model.objects.create_user(**serializer.data)
        return Response(None, status=status.HTTP_201_CREATED)


    



        
