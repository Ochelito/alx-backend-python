from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Only participants of a conversation can view, update, or delete it.
    """

    def has_permission(self, request, view):
        # All API endpoints require authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            # Read-only methods: GET, HEAD, OPTIONS
            if request.method in permissions.SAFE_METHODS:
                return request.user in obj.participants.all()

            # Explicitly handle modification methods
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return request.user in obj.participants.all()

        return False


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Only participants can read messages,
    but only the sender can update or delete their own messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            # Safe read-only methods (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                return request.user in obj.conversation.participants.all()

            # Only the sender can modify their message
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return obj.sender == request.user

        return False
