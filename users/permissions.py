from rest_framework.permissions import BasePermission


class OwnerPermissions(BasePermission):
    message = 'You do not have permission to perform this action.'

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.groups.filter(name='Owner').exists():
            return True

        return False

class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Staff').exists()
        return False

class CustomerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name='Customer').exists()
        return False