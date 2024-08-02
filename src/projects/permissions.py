from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsContributor(BasePermission):
    
    def has_object_permission(self, request, view, obj):       
        return obj.is_contributor(request.user)


class IsAuthorOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.is_author(request.user)