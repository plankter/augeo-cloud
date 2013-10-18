from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:            
            return True

        # Write permissions are only allowed to the owner of the snippet
        return obj.owner == request.user


class IsAuthenticatedNotOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated():
            return False

        # Write permissions are only allowed to the owner of the snippet
        return obj.lot.publisher != request.user