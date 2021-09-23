from django.db import models
from django.contrib.auth.models import UserManager
from django.conf import settings
from django.urls import reverse
from PIL import Image
import re, bcrypt, os

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
        email = User.objects.filter(email=postData.get('user_email'))
        if not email:
            errors['creds'] = "Invalid credentials."
        else:
            logged_user = email[0]
            if not bcrypt.checkpw(postData['user_password'].encode(), logged_user.password.encode()):
                errors['creds'] = "Invalid credentials"
        return errors

def pp_path(instance, filename):
    return '{}/profilePics/{}'.format(instance.media_path(), filename)

class User(models.Model):
    # id
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    image = models.ImageField(default='default.png', upload_to=pp_path)
    # machines = a list of machines associated with a given user
    # files = a list of files associated with a given user
    share = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    def media_path(self):
        user_dir = os.path.join(settings.MEDIA_ROOT, self.last_name + "," + self.first_name)
        if not os.path.exists(user_dir):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, self.last_name + "," + self.first_name, 'profilePics'))
            os.makedirs(os.path.join(settings.MEDIA_ROOT, self.last_name + "," + self.first_name, 'Files'))
        media_path = user_dir
        return media_path
    def save(self, *args, **kwargs):
        self.media_path()
        super(User, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

def folder_path(instance, filename):
    return '{}/Files/{}'.format(instance.owner.media_path(), filename)


class File(models.Model):
    # id
    title = models.CharField(max_length=100, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True, related_name="files", on_delete = models.CASCADE)
    file = models.FileField(null=True, blank=True, upload_to=folder_path)
    content = models.TextField(null=True, blank=True)
    #shared_with = models.ManyToManyField(User, related_name="shared_files", )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    def get_absolute_url(self):
        return reverse('upload', kwargs={'pk': self.pk})


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