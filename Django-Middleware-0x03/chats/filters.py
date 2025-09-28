from django_filters import rest_framework as filters
from chats.models import Message

class MessageFilter(filters.FilterSet):
    """Filter for Message model."""
    conversation = filters.NumberFilter(field_name='conversation__id')
    sender = filters.CharFilter(field_name='sender__username')
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'created_at']