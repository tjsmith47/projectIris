from django.urls import path, re_path
from . import views

urlpatterns = [
    #localhost:8000/
    path('', views.index),
    #localhost:8000/landing
    path('landing', views.land),
    #localhost:8000/landing
    path('viewer', views.viewer),
    #localhost:8000/login
    path('login', views.login),
    #localhost:8000/register
    path('register', views.register),
    #localhost:8000/dashboard
    path('dashboard', views.dash),
    #localhost:8000/files
    path('files', views.files),
    #localhost:8000/appointments/new
    path('files/', views.new, name='new'), 
    #localhost:8000/appointments/new
    path('files/upload', views.upload, name='upload'),
    #localhost:8000/thoughts/1/destroy
    path('file/<int:file_id>/destroy', views.destroy),
    #localhost:8000/logout
    path('logout', views.logout),
    re_path(r'^.*\.html', views.iris_html, name='iris'),
    # The home page
    #path('', views.index, name='index'),
]