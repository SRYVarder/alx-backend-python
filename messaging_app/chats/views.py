

from rest_framework import viewsets
from chats.permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from chats.pagination import MessagePagination
from chats.filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
   
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # This filters the list of objects returned for the 'list' action.
        # It ensures that only conversations where the current user is a participant are returned.
        return self.queryset.filter(participants=self.request.user) 


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_class = MessageFilter

    pagination_class = MessagePagination

    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # This filters the list of objects returned for the 'list' action.
        # It ensures that only messages where the current user is a participant are returned.
        return self.queryset.filter(conversation__participants=self.request.user)


# Create your views here.
