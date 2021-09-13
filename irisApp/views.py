from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Machine
from dotenv import load_dotenv
import bcrypt, os, requests
load_dotenv()

API_KEY = str(os.getenv('API_KEY'))
API_SECRET = str(os.getenv('API_SECRET'))

#localhost:8000/
def index(request):
    return redirect('/viewer')

def viewer(request):
    context = {
        'key' : API_KEY,
        'secret' : API_SECRET,
    }
    return render(request, 'viewer.html', context)

#localhost:8000/landing
def land(request):
    return render(request, 'index.html')
    
#localhost:8000/login
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/landing')
    else:
        logged_user = User.objects.get(email=request.POST['email'])
        request.session.flush()
        request.session['user_id']=logged_user.id
        request.session['first_name']=logged_user.first_name
        return redirect('/thoughts')

#localhost:8000/register
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        print(f'FAILED: {request.POST}')
        for value in errors.values():
            messages.error(request, value)
        return redirect('/landing')
    else:
        password = request.POST['new_password']
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = User.objects.create(
            first_name = request.POST['new_first_name'],
            last_name = request.POST['new_last_name'],
            email = request.POST['new_email'],
            password = pw_hash,
        )
        print(f'CREATE: {request.POST}')
        request.session.flush()
        request.session['user_id'] = new_user.id
        request.session['first_name']=new_user.first_name
        return redirect('/thoughts')

#localhost:8000/thoughts
def dash(request):
    if request.method == "GET":
        if 'user_id' not in request.session:
            return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    thoughts_liked = logged_user.thoughts_liked.all()
    thoughts = Machine.objects.all().order_by('-users_who_like')
    users = User.objects.all(),
    context = {
        'all_thoughts' : thoughts,
        'logged_user' : logged_user,
        'all_users': users,
        'thoughts_liked' : thoughts_liked,
    }
    return render(request, 'dashboard.html', context)

def new(request):
    errors = User.objects.post_validator(request.POST)
    # if errors are present:
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/thoughts')
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        thought = Machine.objects.create(
            message=request.POST['message'],
            posted_by=logged_user
        )
        thought.save()
        print(f'CREATE: {request.POST}')
        return redirect('/thoughts')

def thoughts(request, thought_id):
    logged_user = User.objects.get(id=request.session['user_id'])
    thoughts_liked = logged_user.thoughts_liked.all()
    thought = Machine.objects.get(id=thought_id)
    poster = thought.posted_by.first_name
    all_users = User.objects.all()
    likers = thought.users_who_like.all()
    thoughts = Machine.objects.all().order_by('users_who_like')
    users = User.objects.all(),
    context = {
        'all_thoughts' : thoughts,
        'logged_user' : logged_user,
        'all_users': users,
        'thoughts_liked' : thoughts_liked,
        'thought' : thought,
        'all_users' : all_users,
        'poster' : poster,
        'likers' : likers
    }
    return render(request, 'thoughts.html', context)

def like(request, thought_id):
    thought = Machine.objects.get(id=thought_id)
    logged_user  = User.objects.get(id=request.session['user_id'])
    liked_by = logged_user.thoughts_liked.all()
    if thought in liked_by:
        thought.users_who_like.remove(logged_user)
    else:
        thought.users_who_like.add(logged_user)
    logged_user.save()
    return redirect('/thoughts')

#localhost:8000/thoughts/<thought_id>/delete
def destroy(request, thought_id):
    delete_thought = Machine.objects.get(id=thought_id)
    delete_thought.delete()
    return redirect('/thoughts')

#localhost:8000/logout
def logout(request):
    request.session.flush()
    return redirect('/')