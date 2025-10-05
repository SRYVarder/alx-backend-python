from django.shortcuts import render

from .models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.db.models import Q

def message_history(request, message_id):
    message = Message.objects.get(id=message_id)
    history = message.history.all()
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

def conversation_thread(request, message_id):
    message = Message.objects.select_related('sender', 'receiver').prefetch_related('replies').get(id=message_id)
    # Recursive function to collect all replies
    def get_replies(message, replies_list):
        replies = message.replies.select_related('sender', 'receiver').prefetch_related('replies')
        for reply in replies:
            replies_list.append(reply)
            get_replies(reply, replies_list)
        return replies_list

    all_replies = get_replies(message, [])
    return render(request, 'messaging/conversation_thread.html', {
        'message': message,
        'replies': all_replies
    })

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return HttpResponse("User account deleted")

@login_required
def unread_messages(request):
    messages = Message.objects.filter(receiver=request.user, is_read=False)
    return render(request, 'messaging/unread_messages.html', {'messages': messages})


@cache_page(60)  # Cache for 60 seconds
@login_required
def message_list(request):
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related('sender', 'receiver')
    return render(request, 'messaging/message_list.html', {'messages': messages})
