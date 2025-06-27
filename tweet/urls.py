from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweet_list,name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:pk>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:pk>/delete/', views.tweet_delete, name='tweet_delete'),
    path('<int:pk>/tweet_detail/', views.tweet_detail, name='tweet_detail'),
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login_view'),
]
