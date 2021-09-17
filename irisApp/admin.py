from django.contrib import admin

from .models import User, Machine, File

admin.site.register(User)
admin.site.register(Machine)
admin.site.register(File)
