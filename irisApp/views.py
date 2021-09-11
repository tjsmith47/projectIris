from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Machine
import bcrypt 

#localhost:8000/
def index(request):
    return redirect('/home')

#localhost:8000/home
def home(request):
    context = {
        'all_users':User.objects.all(),
    }
    return render(request, 'index.html', context)

#localhost:8000/login
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/home')
    else:
        logged_user = User.objects.get(email=request.POST['email'])
        #user_id=logged_user.id
        request.session['user_id']=logged_user.id
        return redirect('/dashboard')

def success(request):
    if request.method == "GET":
        return redirect('/')
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'success.html', context)

#localhost:8000/create
def register(request):
    if request.method == "GET":
        return redirect('/home')
    print(f'VALIDATING: {request.POST}')
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        print(f'FAILED: {request.POST}')
        for value in errors.values():
            messages.error(request, value)
        return redirect('/home')
    else:
        password = request.POST['new_password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            first_name = request.POST['new_first_name'],
            last_name = request.POST['new_last_name'],
            email = request.POST['new_email'],
            password = pw_hash,
        )
        print(f'CREATE: {request.POST}')
        request.session.flush()
        user_id = new_user.id
        request.session['user_id'] = user_id
        return redirect(f'/{user_id}/success')

#localhost:8000/<user_id>/dashboard
def dashboard(request):
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'all_machines': Machine.objects.all(),
    }
    return render(request, 'dashboard.html', context)

#localhost:8000/<user_id>/edit
def edit(request):
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'edit.html', context)

#localhost:8000/<user_id>/update
def update(request, user_id):
    #instance = get instance
    logged_user = User.objects.get(id=user_id)
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "GET":
        return render(request, 'edit.html', user_id)
    errors = User.objects.update_validator(request.POST)
    # if errors are present
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/update')
    # if errors not present
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        logged_user.first_name = request.POST['first_name'],
        logged_user.last_name = request.POST['last_name'],
        logged_user.email = request.POST['email'],
        logged_user.password = request.POST['password'],
        logged_user.save()
        user_id = logged_user.id
        messages.success(request, "User information successfully updated")
        return redirect(f'{user_id}/dashboard')

#localhost:8000/logout
def logout(request):
    request.session.flush()
    return redirect('/')