from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOrReadOnly, IsSenderOrReadOnly
from .pagination import StandardResultsSetPagination
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__first_name", "participants__last_name", "participants__email"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user).prefetch_related(
            "participants", "messages"
        )

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return conversation

    @action(detail=True, methods=["post"])
    def add_message(self, request, pk=None):
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        data["conversation"] = str(conversation.conversation_id)
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(conversation=conversation, sender=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ["message_body", "sender__first_name", "sender__last_name"]
    ordering_fields = ["sent_at"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user).select_related(
            "sender", "conversation"
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
