from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Allows listing, retrieving, creating conversations,
    and sending messages to an existing conversation.
    """
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name", "participants__email"]

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        """
        Custom action: Send a message to this conversation.
        Example: POST /conversations/{id}/add_message/
        """
        conversation = self.get_object()
        data = request.data.copy()
        data["conversation"] = str(conversation.conversation_id)

        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    Allows listing all messages or filtering by conversation.
    """
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body", "sender__first_name", "sender__last_name"]

    def list(self, request, *args, **kwargs):
        """
        Optionally filter messages by conversation_id:
        GET /messages/?conversation_id=<uuid>
        """
        conversation_id = request.query_params.get("conversation_id")
        if conversation_id:
            self.queryset = self.queryset.filter(conversation_id=conversation_id)

        return super().list(request, *args, **kwargs)
