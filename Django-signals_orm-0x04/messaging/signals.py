from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """Create a notification whenever a new Message is sent."""
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log old message content before it is updated."""
    if instance.pk:  # update (not new message)
        old_instance = Message.objects.get(pk=instance.pk)
        if old_instance.content != instance.content:
            # Save old content to history
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content
            )
            # Mark message as edited
            instance.edited = True

            # Optional: set edited_by if instance has this info
            # Example: assume you pass instance._edited_by in view
            if hasattr(instance, '_edited_by'):
                instance.edited_by = instance._edited_by
