from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.facebook_login, name='facebook-login'),
    path('callback/', views.facebook_callback, name='facebook-callback'),
]
