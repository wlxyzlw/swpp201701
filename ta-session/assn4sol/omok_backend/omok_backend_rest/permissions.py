from rest_framework import permissions

class RoomsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.username == 'omok_admin'
        return False
