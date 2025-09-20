
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import filters

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sender__first_name', 'message_body']

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Marks a specific message as read and returns a success status.
        """
        try:
            message = self.get_object()
            # In a real application, you would update the message's status here
            # For example: message.is_read = True; message.save()
            
            # Return a 200 OK status to indicate success
            return Response({'status': 'message marked as read'}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            # If the message is not found, return a 404 Not Found status
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)

# Create your views here.


