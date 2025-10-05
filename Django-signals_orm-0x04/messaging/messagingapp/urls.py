"""
URL configuration for messagingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from messaging.views import message_history, delete_user, conversation_thread, unread_messages
from messaging.views import message_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('message/<int:message_id>/thread/', conversation_thread, name='conversation_thread'),
    path('messages/<int:message_id>/history/', message_history, name='message_history'),
    path('unread/', unread_messages, name='unread_messages'),
    path('messages/', message_list, name='message_list'),
    path('delete-account/', delete_user, name='delete_user'),
]
