from rest_framework.permissions import BasePermission

class IsArtist(BasePermission):
    message = "You must be an artist and the owner of this content to perform this action."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_artist

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'artist') and obj.artist == request.user:
            return True
        if hasattr(obj, 'author') and obj.author == request.user:
            return True
        return False


