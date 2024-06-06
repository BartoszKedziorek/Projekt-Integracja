from django.contrib.auth.models import Group
from rest_framework import permissions

def _is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return False

class IsRead(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'read')

class IsExport(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_in_group(request.user, 'export')