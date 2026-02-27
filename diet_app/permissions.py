from rest_framework.permissions import BasePermission

from diet_app.models import User, UserProfile


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if isinstance(obj, User):

            return request.user == obj

        return obj.owner == request.user
    


class ProfileRequired(BasePermission):

    message = "No profile found."

    def has_object_permission(self, request, view, obj):
        return UserProfile.objects.filter(owner=request.user).exists()
    

    
    
    

    
