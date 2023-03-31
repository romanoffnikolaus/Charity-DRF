from rest_framework import permissions


class IsCreatorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
    

class IsDefaultUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type != 'Default user'