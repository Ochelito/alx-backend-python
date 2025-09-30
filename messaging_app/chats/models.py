import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# -----------------------------
# 1. User Model (Custom User)
# -----------------------------
class User(AbstractUser):
    USER_ROLES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.username} ({self.email})"


# -----------------------------
# 2. Conversation Model

class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# -----------------------------
# 3. Message Model
# -----------------------------
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender}"
