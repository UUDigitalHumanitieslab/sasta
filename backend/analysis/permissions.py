from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    # Only owner can edit object
    def has_permission(self, request, view):
        return request.user and request.user.isauthenticated()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    # Owner or admin can edit object
    def has_permission(self, request, view):
        return (request.user or request.user.is_admin) and \
            request.user.isauthenticated()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_admin
