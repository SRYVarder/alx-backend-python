from rest_framework import permissions
from chats.models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation 
    to see, edit, or delete messages/conversation details.
    """
    message = 'You are not a participant of this conversation.'

    def has_permission(self, request, view):
        # Allow only authenticated users to access the API (view-level)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object-level permission check
        # For a Conversation object: check if the user is a participant.
        # For a Message object: check if the user is a participant of the Message's conversation.

        user = request.user

        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=user.pk).exists()

        elif hasattr(obj, 'conversation') and obj.conversation:
            # Assuming 'obj' is a Message instance
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False # Default deny
    