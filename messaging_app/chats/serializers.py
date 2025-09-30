from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with password hashing."""

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'first_name', 'last_name',
            'email', 'phone_number', 'role', 'created_at', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # never return password
        }

    def create(self, validated_data):
        # Ensure password is hashed
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash password if updated
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""

    sender = UserSerializer(read_only=True)  # Show user details instead of just ID
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender',
        write_only=True
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages and participants."""

    participants = UserSerializer(many=True, read_only=True)
    participants_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='participants',
        many=True,
        write_only=True
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participants_id', 'created_at', 'messages']
