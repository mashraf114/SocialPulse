from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.posts_list_create),
    path('facebook/post/', views.facebook_post),
]
