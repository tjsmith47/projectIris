from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import UserManager
#from private_storage.fields import PrivateFileField
from datetime import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['new_email'])
        if email:
            errors['unique'] = 'Email already in use.'
        if not EMAIL_REGEX.match(postData['new_email']):
            errors['regex'] = "Please enter an appropriate email format."
        if len(postData['new_first_name']) < 2 or len(postData['new_last_name']) < 2:
            errors['names'] = "Please enter valid first and last name (>2 characters)."
        if len(postData['new_password']) < 8:
            errors['bad_pass'] = "Please choose a secure password of at least 8 characters."
        if postData['new_password'] != postData['conf_password']:
            errors['pass_match'] = "Passwords do not match, please try again."
        return errors
    def update_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        if len(email) > 1:
            errors['unique'] = 'Email already in use. Please choose another'
        if not EMAIL_REGEX.match(postData['email']):
            errors['badEmail'] = "Invalid email address!"
        if postData['password'] != postData['conf_password']:
            errors['pass'] = "Passwords don't match!"
        if len(postData['password']) < 8:
            errors['badPass'] = "Password must be at least 8 characters long."
        if len(postData['email']) < 3:
            errors['email'] = "Name must be at least 3 characters long."
        return errors
    def login_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['user_email'])
        if not email:
            errors['creds'] = "Invalid credentials."
        else:
            logged_user = email[0]
            if not bcrypt.checkpw(postData['user_password'].encode(), logged_user.password.encode()):
                errors['creds'] = "Invalid credentials"
        return errors
    def add_validator(self, postData):
        errors = {}
        if len(postData['name']) == 0:
            errors['noName'] = 'Please designate a Machine Name.'
        if len(postData['os']) < 5:
            errors['noOS'] = 'Please input an Operating System.'
        return errors

class User(models.Model):
    # id
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    # machines = a list of machines associated with a given user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    objects = UserManager()

class Machine(models.Model):
    # id
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="machines", on_delete = models.CASCADE)
    op_sys = models.CharField(max_length=50, default='macOS 12.0')
    ip_add_local = models.GenericIPAddressField(null=True, blank=True)
    ip_add_remote = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return "{} {} ({})".format(
            self.name, self.owner, self.op_sys
            )

server = FileSystemStorage(location="server/media/")

class File(models.Model):
    # id
    owner = models.ForeignKey(User, related_name="files", on_delete = models.CASCADE)
    #name = models.CharField(max_length=50)
    file = models.FileField(storage=server, upload_to='server/media/')