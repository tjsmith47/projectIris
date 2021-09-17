from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files import File
from .models import User, Machine, File
from dotenv import load_dotenv
import bcrypt, os, datetime, requests
load_dotenv()

API_KEY = str(os.getenv('API_KEY'))
API_SECRET = str(os.getenv('API_SECRET'))

#localhost:8000/
def index(request):
    return redirect('/landing')

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
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        logged_user = User.objects.get(email=request.POST['user_email'])
        request.session['user_id'] = logged_user.id
        request.session['first_name'] = logged_user.first_name
        return redirect('/dashboard')

#localhost:8000/register
def register(request):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['new_password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['new_first_name'],
            last_name = request.POST['new_last_name'],
            email = request.POST['new_email'],
            password = pw_hash,
        )
        print(f'CREATE: {request.POST}')
        request.session['user_id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        return redirect('/dashboard')

#localhost:8000/dashboard
def dash(request):
    if request.method == "GET":
        if 'user_id' not in request.session:
            return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    machines = Machine.objects.all(),
    context = {
        'user' : logged_user,
        'all_machines': machines,
    }
    return redirect('/files')
    #return render(request, 'iris/dashboard.html', context)

#localhost:8000/files
def files(request):
    context = {
        'user_files' : File.objects.filter(owner=User.objects.get(id=request.session['user_id'])),
    }
    return render(request, 'iris/form_upload.html', context)

#localhost:8000/files/upload
def upload(request):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    """ errors = User.objects.add_validator(request.POST)
    # if errors are present:
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/devices/new') 
    else:"""
    logged_user = User.objects.get(id=request.session['user_id'])
    file = File.objects.create(
        file=request.POST['new'],
        #name=request.POST['new_file'],
        owner=logged_user
    )
    file.save()
    return redirect('/dashboard')

#localhost:8000/appointments/new
def new(request):
    context = {
        'status' : Machine.objects.all(),
    }
    return render(request, 'form_upload.html', context)

#localhost:8000/appointments/create
def create(request):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    errors = User.objects.post_validator(request.POST)
    # if errors are present:
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/devices/new')
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        appt = Machine.objects.create(
            task=request.POST['task'],
            date=request.POST['date'],
            user=logged_user
        )
        appt.save()
        print(f'CREATE: {request.POST}')
        return redirect('/dashboard')

def thoughts(request, thought_id):
    logged_user = User.objects.get(id=request.session['user_id'])
    thought = Machine.objects.get(id=thought_id)
    all_users = User.objects.all()
    users = User.objects.all(),
    context = {
        'all_thoughts' : thoughts,
        'logged_user' : logged_user,
        'all_users': users,
        'all_users' : all_users,
    }
    return render(request, 'thoughts.html', context)

#localhost:8000/appointments/1/edit
def edit(request, appt_id):
    appt = Machine.objects.get(id=appt_id)
    status = Machine.objects.all()
    context = {
        'appt' : appt,
        'status' : status,
    }
    return render(request, 'edit.html', context)

#localhost:8000/appointments/1/update
def update(request, appt_id, stat_id):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    errors = User.objects.post_validator(request.POST)
    # if errors are present
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect(f'appointments/{appt_id}/edit')
    # if errors not present
    else:
        status = Machine.objects.filter(id=stat_id)
        appt = Machine.objects.get(id=appt_id)
        appt.task = request.POST['task'],
        appt.date = request.POST['date'],
        appt.status = status
        appt.save()
        return redirect('/dashboard')

#localhost:8000/thoughts/<thought_id>/delete
def destroy(request, thought_id):
    delete_device = Machine.objects.get(id=thought_id)
    delete_device.delete()
    return redirect('/dashboard')

#localhost:8000/logout
def logout(request):
    request.session.flush()
    return redirect('/')

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    context = {}
    template = loader.get_template('app/index.html')
    return HttpResponse(template.render(context, request))


def iris_html(request):
    context = {
        'user_files' : File.objects.filter(owner=User.objects.get(id=request.session['user_id'])),
    }
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('iris/' + load_template)
    return HttpResponse(template.render(context, request))
