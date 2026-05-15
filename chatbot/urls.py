from django.urls import path
from . import views

urlpatterns = [
    path('',              views.chat_view,    name='chat'),
    path('api/message/',  views.send_message, name='send-message'),
    path('api/clear/',    views.clear_chat,   name='clear-chat'),
]
