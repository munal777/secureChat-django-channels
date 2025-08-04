from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from chat.views import landing_page_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page_view, name='landing_page'),
    path('chat/', include('chat.urls')),
    path('accounts/', include('accounts.urls')),
]
