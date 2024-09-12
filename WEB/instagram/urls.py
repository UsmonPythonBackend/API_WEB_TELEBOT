from django.contrib import admin
from django.urls import path, include
from .views import HomeView, PostView, CommentsView, RegisterView, LoginView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/', PostView.as_view(), name='posts'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

]
