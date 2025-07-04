from django.urls import path
from .views import chat_view, dashboard_view, landing_page_view

urlpatterns = [
    path('chat/<str:room_name>/', chat_view, name='chat_room'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', landing_page_view, name='landing_page'),
]