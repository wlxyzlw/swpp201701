from rest_framework import permissions

class DebtPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.username == 'debt_admin':
            return True
        if request.method == 'GET':
            return obj.borrower == request.user or obj.lender == request.user
        if request.method == 'DELETE':
            return obj.lender == request.user
        return False

class DebtsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.username == 'debt_admin'
        if request.method == 'POST':
            return True # IsAuthenticated will work
        return False

class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.username == 'debt_admin':
            return True
        return obj == request.user

class UsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.username == 'debt_admin':
            return True
        return False
