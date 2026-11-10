from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='detector/login.html'), name='login'),
    path('dashboard/', views.index, name='index'),
    path('inventario/', views.inventario, name='inventario'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('logout/', LogoutView.as_view(), name='logout'),
]