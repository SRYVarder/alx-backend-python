from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if message already exists (i.e., it's an update)
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:  # Content changed
            instance.edited = True
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Messages and notifications are already deleted via CASCADE
    # Optionally log the deletion or perform additional cleanup
    print(f"User {instance.username} deleted, related data cleaned up")