from django.urls import path
from . import views

urlpatterns = [

    path('callback/', views.callback_view, name='tiktok-callback'),
    path('upload/', views.upload_video_view, name='tiktok-upload'),

]
