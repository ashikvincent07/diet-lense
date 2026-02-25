from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework import authentication, permissions

from diet_app.serializers import UserSerializer, UserProfileSerializer
from diet_app.permissions import IsOwner
from diet_app.models import UserProfile, User



class UserRegisterView(CreateAPIView):
    
    permission_classes = [permissions.AllowAny]

    serializer_class = UserSerializer



class UserRetrieveView(RetrieveAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    serializer_class = UserSerializer

    queryset = User.objects.all()



class UserProfileCreateView(CreateAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):

    #     validated_data = serializer.validated_data

    #     cal = daily_calorie_consumption(height=validated_data.get("height"), weight=validated_data.get("weight"),
    #                                     age=validated_data.get("age"), gender=validated_data.get("gender"),
    #                                     activity_level=float(validated_data.get("activity_level", 1.2)))

        return serializer.save(owner=self.request.user)
    


class UserProfileRetrieveView(RetrieveAPIView, UpdateAPIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.all()
        





