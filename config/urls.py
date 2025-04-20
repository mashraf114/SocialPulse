from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("<h1> Django Backend is Running</h1>")

urlpatterns = [
    path('', home), 
    path('admin/', admin.site.urls),
    path('api/', include('posts.urls')),
]
