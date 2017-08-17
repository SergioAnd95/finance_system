from rest_framework.permissions import BasePermission


class IsClientPermission(BasePermission):
    """ Permission for Client """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and not request.user.is_manager
            and request.user.is_active
        )


class ClientHavePINPermission(BasePermission):
    """ Permission for Client that have PIN """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and not request.user.is_manager
            and request.user.is_active
            and request.user.password
        )


class IsManagerPermission(BasePermission):
    """ Permission for Manager """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_manager or request.user.is_superuser)
            and request.user.is_active
            )
