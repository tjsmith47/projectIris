from django.urls import path
from . import views

urlpatterns = [
    #localhost:8000/
    path('', views.index),
    #localhost:8000/landing
    path('landing', views.land),
    #localhost:8000/login
    path('login', views.login),
    #localhost:8000/register
    path('register', views.register),
    #localhost:8000/thoughts
    path('thoughts', views.dash),
    #localhost:8000/thoughts
    path('thoughts/new', views.new),
    #localhost:8000/thoughts/1
    path('thoughts/<int:thought_id>', views.thoughts),
    #localhost:8000/thoughts/1/like
    path('thoughts/<int:thought_id>/like', views.like),
    #localhost:8000/thoughts/1/destroy
    path('thoughts/<int:thought_id>/destroy', views.destroy),
    #localhost:8000/logout
    path('logout', views.logout),
]