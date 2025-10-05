
from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class NotificationSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass')
        self.receiver = User.objects.create_user(username='receiver', password='pass')

    def test_notification_created_on_message_save(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )
        notification = Notification.objects.get(user=self.receiver, message=message)
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.user, self.receiver)

def test_message_edit_logging(self):
    message = Message.objects.create(
        sender=self.sender,
        receiver=self.receiver,
        content="Original"
    )
    message.content = "Updated"
    message.save()
    history = MessageHistory.objects.get(message=message)
    self.assertEqual(history.old_content, "Original")
    self.assertTrue(message.edited) 

def test_user_deletion_cleanup(self):
    message = Message.objects.create(
        sender=self.sender,
        receiver=self.receiver,
        content="Test"
    )
    notification = Notification.objects.create(user=self.receiver, message=message)
    history = MessageHistory.objects.create(message=message, old_content="Old")
    self.sender.delete()
    self.assertFalse(Message.objects.filter(sender=self.sender).exists())
    self.assertFalse(Notification.objects.filter(user=self.sender).exists())
    self.assertFalse(MessageHistory.objects.filter(message__sender=self.sender).exists())   
    
def test_threaded_conversation(self):
    message = Message.objects.create(
        sender=self.sender,
        receiver=self.receiver,
        content="Main message"
    )
    reply = Message.objects.create(
        sender=self.receiver,
        receiver=self.sender,
        content="Reply",
        parent_message=message
    )
    messages = Message.objects.prefetch_related('replies').filter(id=message.id)
    self.assertEqual(messages[0].replies.first().content, "Reply")

def test_unread_messages_manager(self):
    Message.objects.create(sender=self.sender, receiver=self.receiver, content="Read", read=True)
    unread_message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Unread")
    unread = Message.unread_objects.unread_for_user(self.receiver)
    self.assertEqual(unread.count(), 1)
    self.assertEqual(unread.first().content, "Unread")

def test_message_list_cache(self):
    self.client.login(username='receiver', password='pass')
    response1 = self.client.get('/messages/')
    cache_key = 'views.decorators.cache.cache_page.message_list.GET.' + response1.wsgi_request.build_absolute_uri().replace('http://testserver', '')
    cached_response = cache.get(cache_key)
    self.assertIsNotNone(cached_response)

    # Create your tests here.
