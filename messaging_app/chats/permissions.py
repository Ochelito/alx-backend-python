from rest_framework import permissions
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users
    - Only participants of a conversation can access/modify it
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        obj can be a Conversation or a Message.
        - Allow access only if request.user is a participant.
        """
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If obj is a Message, check conversation participants
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
