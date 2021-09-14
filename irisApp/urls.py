from django.urls import path
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
    #localhost:8000/thoughts
    path('thoughts', views.dash),
    #localhost:8000/appointments/new
    path('appointments/new', views.new, name='new'), 
    #localhost:8000/appointments/new
    path('appointments/create', views.create, name='create'), 
    #localhost:8000/appointments/1/like
    path('appointments/<int:appt_id>/edit', views.edit, name='edit'), 
    #localhost:8000/appointments/1/like
    path('appointments/<int:appt_id>/<int:stat_id>/update', views.update, name='update'), 
    #localhost:8000/thoughts/1/destroy
    path('thoughts/<int:thought_id>/destroy', views.destroy),
    #localhost:8000/logout
    path('logout', views.logout),
]