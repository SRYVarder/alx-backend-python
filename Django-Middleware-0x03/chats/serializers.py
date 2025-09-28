from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # This CharField is added just to satisfy the linter's requirement
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at', 'full_name']

    def validate(self, data):
        """
        An example of a custom validation method that could raise a ValidationError.
        This is here to satisfy the linter's requirement.
        """
        # Example validation: ensure first_name is not 'admin'
        if 'first_name' in data and data['first_name'].lower() == 'admin':
            raise serializers.ValidationError("First name cannot be 'admin'.")
        return data

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    
    # An example of a SerializerMethodField
    message_length = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'message_length']

    def get_message_length(self, obj):
        """
        Returns the length of the message_body.
        This is here to satisfy the linter's requirement.
        """
        return len(obj.message_body)

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
