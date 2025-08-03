from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def test_view(request):
    return HttpResponse("Django is working!")

urlpatterns = [
    path('admin/', admin.site.urls),
      path('', test_view),
    # path('', include('chat.urls')),
    # path('', include('accounts.urls')),
]
