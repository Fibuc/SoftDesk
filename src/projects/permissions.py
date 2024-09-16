from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsContributor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_contributor(request.user)


class CanModifyResource(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT']:
            return obj.author == request.user

        return True


class CanDeleteResource(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.author == request.user

        return True


class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.is_author(request.user)
