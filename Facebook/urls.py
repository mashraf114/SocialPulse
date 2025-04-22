from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.facebook_login, name='facebook-login'),
    path('callback/', views.facebook_callback, name='facebook-callback'),
    path('profile/', views.facebook_profile, name='facebook-profile'),
    path('disconnect/', views.facebook_disconnect, name='facebook-disconnect'),
    path('post/', views.facebook_post, name='facebook-post'),
    path('pages/', views.facebook_pages, name='facebook-pages'),
    path('success/', views.facebook_success, name='facebook-success'),
]
