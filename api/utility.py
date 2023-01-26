from rest_framework.response import Response
from rest_framework import status
import inspect

def authenticated(func):

    def wrapper_func(*args, **kwargs):
        # Finding value of 'request' parameter
        args_name = inspect.getfullargspec(func)[0]
        args_dict = dict(zip(args_name, args))
        request = args_dict['request']

        # Checking if user is authenticated
        if request.user.is_authenticated:
            return func(*args, **kwargs)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)
    return wrapper_func

