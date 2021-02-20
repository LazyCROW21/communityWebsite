from django.urls import path
from . import views

urlpatterns = [
    path('idkwhat/', views.sendWelcomeMail),
    path('all_blogs/', views.blogs),
    path('all_users/', views.users),
    path('user/<int:pk>/', views.get_user),
    path('<slug:slug>/', views.get_blog),
]
