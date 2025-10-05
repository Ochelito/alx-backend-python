from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification
from .models import Message, Notification, MessageHistory

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

class MessageEditSignalTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="pass")
        self.bob = User.objects.create_user(username="bob", password="pass")
        self.msg = Message.objects.create(sender=self.alice, receiver=self.bob, content="Hello Bob!")

    def test_message_edit_creates_history(self):
        # Edit the message
        self.msg.content = "Hello Bob! (edited)"
        self.msg.save()

        history = MessageHistory.objects.filter(message=self.msg)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, "Hello Bob!")
        self.assertTrue(self.msg.edited)
