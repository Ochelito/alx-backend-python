from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with password hashing and validation."""

    #CharField for password (write only)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'first_name', 'last_name',
            'email', 'phone_number', 'role', 'created_at', 'password'
        ]
        extra_kwargs = {
            'email': {'required': True},  # force validation
        }

    def validate_email(self, value):
        """Ensure email is unique and lowercase."""
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        # Ensure password is hashed
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash password if updated
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with sender details."""

    sender = serializers.SerializerMethodField()
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender',
        write_only=True
    )

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'message_body', 'sent_at']

    def get_sender(self, obj):
        """Return sender basic info."""
        return {
            "user_id": obj.sender.user_id,
            "first_name": obj.sender.first_name,
            "last_name": obj.sender.last_name,
            "email": obj.sender.email
        }


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
