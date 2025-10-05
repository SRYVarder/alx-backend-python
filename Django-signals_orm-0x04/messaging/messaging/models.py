
from django.db import models
from django.contrib.auth.models import User

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.filter(receiver=user, read=False).only('id', 'content', 'sender__username', 'timestamp')

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  
    parent_message = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies') 
    read = models.BooleanField(default=False) 
    objects = models.Manager()  # Default manager
    unread_objects = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='User')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} about message {self.message.id}"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} at {self.edited_at}"   