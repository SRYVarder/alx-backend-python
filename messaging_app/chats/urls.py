

from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include, routers.DefaultRouter()

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls

