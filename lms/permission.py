from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or obj.user == request.user


class BookReturnPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "PATCH":
            return obj.student == request.user
        return False
