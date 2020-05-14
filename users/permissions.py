from rest_framework import permissions


class IsShopAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsShopAdminOrGetSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.id == obj.id:
            return True
        return request.user.is_admin
