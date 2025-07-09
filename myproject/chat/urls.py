from django.urls import path
from .views import chat_view, dashboard_view, landing_page_view, create_group_view, leave_group_view

urlpatterns = [
    path('chat/<str:room_name>/', chat_view, name='chat_room'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', landing_page_view, name='landing_page'),
    path('create-group/', create_group_view, name='create_group'),
    path('leave-group/', leave_group_view, name='leave_group'),
]