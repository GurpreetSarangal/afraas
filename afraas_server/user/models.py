from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=255)


class Shift(models.Model):
    time_in = models.TimeField()
    time_out = models.TimeField()


class User(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)


