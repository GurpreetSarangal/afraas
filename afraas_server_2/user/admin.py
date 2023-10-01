from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm
from .models import User

# @admin.register(User)
# class MyUserAdmin(UserAdmin):
#     add_form = MyUserCreationForm
    
#     ordering = ['id']

# Register your models here.
admin.site.register(Department)
admin.site.register(Shift)
admin.site.register(User)