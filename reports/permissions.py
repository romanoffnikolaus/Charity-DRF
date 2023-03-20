from rest_framework import permissions

from charity_programs.models import Program

class IsProgramOwnerOrReadOnly(permissions.BasePermission):
    message = 'Only the user who created the program can create a report.'

    def has_permission(self, request, view):
        program_slug = request.data.get('program')
        if Program.objects.filter(user=request.user, slug=program_slug).exists():
            return True
        return False
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You do not have permission to update information. That is not your report.'
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user

    