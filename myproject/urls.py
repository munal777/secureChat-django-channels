from django.contrib import admin
from django.urls import path, include
from chat.views import landing_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='landing_page'),
    path('app/', include('chat.urls')),
    path('accounts/', include('accounts.urls')),
]
