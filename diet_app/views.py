from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from rest_framework import authentication, permissions

from diet_app.serializers import UserSerializer


class UserRegisterView(CreateAPIView):
    
    permission_classes = [permissions.AllowAny]

    serializer_class = UserSerializer
    


