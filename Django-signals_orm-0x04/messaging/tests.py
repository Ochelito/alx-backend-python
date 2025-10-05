from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class NotificationSignalTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="password123")
        self.bob = User.objects.create_user(username="bob", password="password123")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="Hello Bob!"
        )
        notification = Notification.objects.get(user=self.bob, message=msg)
        self.assertFalse(notification.is_read)
