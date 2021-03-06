from django.urls import path
from .views import (
    FileCreateView,
    FileUpdateView,
)
from . import views

urlpatterns = [
    #localhost:8000/
    path('', views.index),
    #localhost:8000/landing
    path('landing', views.land),
    #localhost:8000/login
    path('login', views.login, name='login'),
    #localhost:8000/register
    path('register', views.register, name='reg'),
    #localhost:8000/dashboard
    path('dashboard', views.dash, name='dash'),
    #localhost:8000/gallery
    path('gallery', views.gallery, name='gallery'),
    #localhost:8000/files
    path('files', FileCreateView.as_view(), name='new'), 
    #localhost:8000/files/1/update
    path('file/<int:pk>/update', FileUpdateView.as_view(), name='update'), 
    #localhost:8000/files/upload
    path('files/upload', views.upload, name='upload'),
    #localhost:8000/files/1/destroy
    path('file/<int:file_id>/destroy', views.destroy, name="delete"),
    #localhost:8000/logout
    path('logout', views.logout),
]