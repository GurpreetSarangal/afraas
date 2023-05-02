from django.db import models
from django.contrib.auth.models import AbstractUser,  PermissionsMixin, Group, Permission
from .manager import UserManager
from django.contrib.auth.hashers import make_password

# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Shift(models.Model):
    id = models.AutoField(primary_key=True)
    time_in = models.TimeField()
    time_out = models.TimeField()

    def __str__(self):
        return f"{self.id} timing -> {self.time_in} - {self.time_out}"


class User(AbstractUser, PermissionsMixin):
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, default="NA")
    is_registered = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    
    
    USERNAME_FIELD = 'email'

    objects = UserManager()

    REQUIRED_FIELDS = ['name']

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='myuser_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='myuser_set',
        related_query_name='user',
    )
    
