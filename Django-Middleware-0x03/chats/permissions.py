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
        # Explicitly handle PUT, PATCH, and DELETE methods to allow updates and deletions only by participants.

        user = request.user

        # Allow read-only access (GET, HEAD, OPTIONS) for participants
        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Conversation):
                return obj.participants.filter(pk=user.pk).exists()
            elif hasattr(obj, 'conversation') and obj.conversation:
                return obj.conversation.participants.filter(pk=user.pk).exists()
            return False

        # Explicitly handle PUT, PATCH, and DELETE methods
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if isinstance(obj, Conversation):
                return obj.participants.filter(pk=user.pk).exists()
            elif hasattr(obj, 'conversation') and obj.conversation:
                return obj.conversation.participants.filter(pk=user.pk).exists()
            return False

        # Allow other methods (e.g., POST) if the user is a participant
        if isinstance(obj, Conversation):
            return obj.participants.filter(pk=user.pk).exists()
        elif hasattr(obj, 'conversation') and obj.conversation:
            return obj.conversation.participants.filter(pk=user.pk).exists()

        return False  # Default deny
