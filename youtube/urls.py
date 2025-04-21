# urls.py
from django.urls import path
from .views import YouTubeUploadView, YouTubeAuthView, YouTubeCallbackView

urlpatterns = [
    path("youtube/", YouTubeUploadView.as_view(), name="youtube_upload"),
    path("youtube/auth/", YouTubeAuthView.as_view(), name="youtube_auth"),
    path("youtube/callback/", YouTubeCallbackView.as_view(), name="youtube_callback"),
]
