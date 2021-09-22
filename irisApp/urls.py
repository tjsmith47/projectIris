from django.urls import path
from .views import (
    PostCreateView,
)
from . import views

urlpatterns = [
    #localhost:8000/
    path('', views.index),
    #localhost:8000/landing
    path('landing', views.land),
    #localhost:8000/landing
    path('viewer', views.viewer),
    #localhost:8000/login
    path('login', views.login, name='login'),
    #localhost:8000/register
    path('register', views.register, name='reg'),
    #localhost:8000/dashboard
    path('dashboard', views.dash, name='dash'),
    #localhost:8000/files
    path('gallery', views.gallery, name='gallery'),
    #localhost:8000/appointments/new
    path('files', PostCreateView.as_view(), name='new'), 
    #localhost:8000/appointments/new
    path('files/upload', views.upload, name='upload'),
    #localhost:8000/thoughts/1/destroy
    path('file/<int:file_id>/destroy', views.destroy, name="delete"),
    #localhost:8000/logout
    path('logout', views.logout),
]