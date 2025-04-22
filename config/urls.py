from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("facebook/", include("Facebook.urls")),
    path("api/", include("youtube.urls")),
]
