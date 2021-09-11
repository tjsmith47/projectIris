from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('login', views.login),
    path('create', views.register),
    path('success', views.success),
    path('dashboard', views.dashboard),
    path('<int:user_id>/edit', views.edit),
    path('<int:user_id>/update', views.update),
    path('logout', views.logout),
]