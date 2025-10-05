from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to fetch unread messages for a specific user,
    retrieving only necessary fields.
    """
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only(
            'id', 'sender', 'content', 'timestamp', 'parent_message'
        )
