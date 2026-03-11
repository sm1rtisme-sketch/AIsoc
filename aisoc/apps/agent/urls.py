from django.urls import path
from . import views

app_name = 'agent'

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('stream-chat', views.stream_chat, name='stream_chat'),
]
