from django.contrib.auth.models import (
    User
    )
from rest_framework import generics
from .serializers import (
    UserSerializer
    )

class UserCreateView(generics.ListCreateAPIView):
    """
        Allowed HTTP Method:
            - POST
            - GET
        Using the built in ListCreateAPIView which provides
        functionality for GET and POST Request
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer