from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Router for chats app
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
