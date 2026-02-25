from rest_framework.permissions import BasePermission

from diet_app.models import User


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if isinstance(obj, User):

            return request.user == obj

        return obj.owner == request.user
    

    
