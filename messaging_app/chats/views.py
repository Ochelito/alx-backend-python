from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOrReadOnly, IsSenderOrReadOnly


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Only participants can view or update their conversations.
    """
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name", "participants__email"]
    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]

    def get_queryset(self):
        """Limit conversations to those the current user participates in."""
        return Conversation.objects.filter(participants=self.request.user).prefetch_related(
            "participants", "messages"
        )

    def perform_create(self, serializer):
        """Add the requesting user as a participant in the new conversation."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return conversation

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Custom action: Send a message to this conversation.
        Example: POST /conversations/{id}/add_message/
        """
        conversation = self.get_object()

        # Ensure the requesting user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        data["conversation"] = str(conversation.conversation_id)

        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Users only see messages in conversations they belong to.
    """
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body", "sender__first_name", "sender__last_name"]
    permission_classes = [IsAuthenticated, IsSenderOrReadOnly]

    def get_queryset(self):
        """Show only messages from conversations where the user is a participant."""
        return Message.objects.filter(conversation__participants=self.request.user).select_related(
            "sender", "conversation"
        )

    def perform_create(self, serializer):
        """Force the sender to be the logged-in user."""
        serializer.save(sender=self.request.user)
