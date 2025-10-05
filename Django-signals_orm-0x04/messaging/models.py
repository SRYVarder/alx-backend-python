from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False) 
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    objects = models.Manager()
    unread = UnreadMessagesManager() 

    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"
        
    def get_thread(self):
        """
        Recursive method to fetch all replies in a threaded conversation.
        """
        thread = []
        for reply in self.replies.all().select_related('sender', 'receiver').prefetch_related('replies'):
            thread.append(reply)
            thread.extend(reply.get_thread())
        return thread

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_messages')

    def __str__(self):
        return f"Edit history of Message ID {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID {self.message.id}"
