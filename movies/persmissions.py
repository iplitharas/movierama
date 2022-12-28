"""IsAuthorOrReadOnly permission implementation """
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission for checking if an authenticated user
    can edit/delete a movie
    """

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Return `True` if permission is granted, otherwise `False`
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        # only the author can edit
        return obj.author == request.user
