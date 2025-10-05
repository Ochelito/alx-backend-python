from rest_framework import permissions

class IsParticipantOrReadOnly(permissions.BasePermission):
    """
    Allow access only if the user is a participant in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Allow access only if the user is the sender of the message.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
