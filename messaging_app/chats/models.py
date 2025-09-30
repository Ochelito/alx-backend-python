import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

# -----------------------------
# 1. User Model (Custom User)
# -----------------------------
class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds UUID, phone_number, role, and created_at.
    Keeps password from AbstractUser (already hashed).
    """

    USER_ROLES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    # Override default reverse accessors to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",   # avoids clash with auth.User.groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",   # avoids clash with auth.User.user_permissions
        blank=True
    )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    @property
    def password_hash(self):
        """
        Alias for compatibility with the schema.
        Returns the hashed password stored in `password`.
        """
        return self.password

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# -----------------------------
# 2. Conversation Model

class Conversation(models.Model):
    """
    Tracks conversations between multiple users.
    Many-to-Many relationship with User (participants).
    """

    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"

# -----------------------------
# 3. Message Model
# -----------------------------
class Message(models.Model):
    """
    Represents a message sent by a user within a conversation.
    """

    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        related_name='messages_sent',
        on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE
    )
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"
