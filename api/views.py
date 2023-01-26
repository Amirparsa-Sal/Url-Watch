from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import UserRegisterSerializer, UrlSerializer, UrlCompactSerializer, WarningSerializer
from api.utility import authenticated
from api.models import Url, Warning

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
        self.user_model.objects.create_user(**serializer.data)
        return Response(None, status=status.HTTP_201_CREATED)


class UrlRegisterViewSet(ViewSet):
    '''A view for working with entered urls for a user'''

    authentication_classes = (JWTAuthentication,)

    @authenticated
    def create(self, request):
        ''' POST: /api/url/ '''
        print("here")
        serializer = UrlSerializer(data=request.data)
        # Check if the user input is valid
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # check if user has created 20 urls
        if request.user.urls.count() >= 20:
            return Response({'error': 'You have reached the maximum number of urls'}, status=status.HTTP_400_BAD_REQUEST)
        # create the url
        serializer.save(user=request.user)
        return Response(None, status=status.HTTP_201_CREATED)

    @authenticated
    def list(self, request):
        ''' GET: /api/url/ '''
        serializer = UrlCompactSerializer(request.user.urls.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @authenticated
    def retrieve(self, request, pk=None):
        ''' GET: /api/url/<pk> '''
        # check if the url exists and belongs to the user
        try:
            url = request.user.urls.get(pk=pk)
        except Url.DoesNotExist:
            return Response({'error': 'Url does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # return the url
        serializer = UrlSerializer(url)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @authenticated
    def delete(self, request, pk=None):
        ''' DELETE: /api/url/<pk> '''
        # check if the url exists and belongs to the user
        try:
            url = request.user.urls.get(pk=pk)
        except Url.DoesNotExist:
            return Response({'error': 'Url does not exist'}, status=status.HTTP_404_NOT_FOUND)
        # delete the url
        url.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class WarningViewset(ViewSet):
    '''A view for working with warnings for a user'''

    authentication_classes = (JWTAuthentication,)

    @authenticated
    def list(self, request):
        ''' GET: /api/url/warning '''
        # join the url and warning tables
        warnings = Warning.objects.filter(url__user=request.user)
        # return the warnings
        serializer = WarningSerializer(warnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)