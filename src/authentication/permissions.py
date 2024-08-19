from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_account_owner(request.user)
