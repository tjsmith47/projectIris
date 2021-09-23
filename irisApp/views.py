from django.shortcuts import render, redirect
from django.contrib.staticfiles.views import serve
from django.contrib import messages
from django.views.generic import (
    CreateView,
    UpdateView,
)
from .models import User, File
from dotenv import load_dotenv
import bcrypt, os
load_dotenv()

API_KEY = str(os.getenv('API_KEY'))
API_SECRET = str(os.getenv('API_SECRET'))

#localhost:8000/
def index(request):
    return redirect('/landing')

def getfile(request):
    return serve(request, 'file')

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
        logged_user.media_path()
        request.session['user_id'] = logged_user.id
        request.session['first_name'] = logged_user.first_name
        request.session['last_name'] = logged_user.last_name
        request.session['image'] = logged_user.image.url
        print(f"SUCCESS: {logged_user.first_name, logged_user.media_path()}")
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
        new_user.media_path()
        request.session['user_id'] = new_user.id
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['image'] = new_user.image.url
        return redirect('/dashboard')

#localhost:8000/dashboard
def dash(request):
    if request.method == "GET":
        if 'user_id' not in request.session:
            return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : logged_user,
        'user_files' : File.objects.filter(owner=User.objects.get(id=request.session['user_id'])),
    }
    return redirect('/files')

#localhost:8000/gallery
def gallery(request):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    user_files = File.objects.filter(owner=logged_user)
    print(user_files)
    context = {
        'user' : logged_user,
        'user_files' : user_files
    }
    return render(request, 'iris/media_gallery.html', context)

#localhost:8000/files
class FileCreateView(CreateView):
    model = File
    template_name = 'iris/form_upload.html'
    fields = ['title', 'file', 'content']
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class FileUpdateView(UpdateView):
    model = File
    template_name = 'iris/form_upload.html'
    fields = ['title', 'file', 'content']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.owner:
            return True
        return False

#localhost:8000/files/upload
def upload(request):
    if request.method == 'GET':
        if 'user_id' not in request.session:
            return redirect('/')
    logged_user = User.objects.get(id=request.session['user_id'])
    file = File.objects.create(
        title=request.POST['title'],
        owner=logged_user,
        content=request.POST['content'],
        file = request.FILES['file']
    )
    file.save()
    print('SUCCESS: ' + file.file.name)
    return redirect('/gallery')

#localhost:8000/file/<file_id>/delete
def destroy(request, file_id):
    delete_file = File.objects.get(id=file_id)
    delete_file.delete()
    messages.success(request, "Successfully deleted!")
    return redirect('/gallery')

#localhost:8000/logout
def logout(request):
    request.session.flush()
    return redirect('/')