

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('tiktok_integration.urls')),  
    path('tiktok/', include('tiktok_integration.urls')),
    path('api/tiktok/refresh/', views.refresh_token_view, name='tiktok-refresh'),


]
