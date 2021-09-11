from django.db import models
import re, bcrypt 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['new_email'])
        if email:
            errors['unique'] = 'Email already in use.'
        if not EMAIL_REGEX.match(postData['new_email']):
            errors['badEmail'] = "Invalid email address!"
        if len(postData['new_first_name']) < 3:
            errors['first'] = "First name must be at least 2 characters long."
        if len(postData['new_last_name']) < 3:
            errors['last'] = "Last name must be at least 2 characters long."
        if len(postData['new_password']) < 8:
            errors['badPass'] = "Password must be at least 8 characters long."
        if postData['new_password'] != postData['conf_password']:
            errors['pass'] = "Passwords don't match!"
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
        """ if postData['admin'] != True or postData['admin'] != False:
            errors['admin'] = "Must select if petitioning for admin." """
        return errors
    def login_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        if not email:
            errors['email'] = "You are not in the database"
        else:
            logged_user = email[0]
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password):
                errors['creds'] = "Invalid Credentials"
        return errors

class User(models.Model):
    # id
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    # machines = a list of machines associated with a given user
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        if self.admin == True:
            return "ADMIN USER: {} {} | Email: {} | Password: {}".format(
                self.first_name, self.last_name, self.email, self.password
                )
        else:
            return "Name: {} {} | Email: {} | Password: {}".format(
                self.first_name, self.last_name, self.email, self.password
                )
    objects = UserManager()

class Machine(models.Model):
    # id
    owner = models.ForeignKey(User, related_name="machines", on_delete = models.CASCADE)
    brand = models.CharField(max_length=50, default='Apple')
    model = models.CharField(max_length=50)
    op_sys = models.CharField(max_length=50, default='macOS 12.0')
    cpu = models.CharField(max_length=50)
    memory = models.IntegerField()
    mem_type = models.BooleanField(default=False)
    storage = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        if self.mem_type == False:
            return "{}'s {} ({}). Specs: OS - {}, CPU - {}, RAM - {}GB, Storpassword - {}".format(
                self.owner, self.model, self.brand, self.op_sys, self.cpu, self.memory, self.storage
                )
        else:
            return "{}'s {} ({}). Specs: OS - {}, CPU - {}, RAM - {}TB, Storpassword - {}".format(
                self.owner, self.model, self.brand, self.op_sys, self.cpu, self.memory, self.storage
                )
