from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chats.permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from chats.pagination import MessagePagination
from chats.filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Filter conversations where the current user is a participant
        return self.queryset.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Explicitly use Message.objects.filter to ensure messages are filtered
        # by conversations where the user is a participant
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        
        # Filter by conversation_id if provided in query parameters
        conversation_id = self.request.query_params.get('conversation_id', None)
        if conversation_id:
            queryset = Message.objects.filter(
                conversation__participants=self.request.user,
                conversation__id=conversation_id
            )
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the user is a participant in the conversation
        conversation_id = serializer.validated_data.get('conversation').id
        if not Conversation.objects.filter(id=conversation_id, participants=self.request.user).exists():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
