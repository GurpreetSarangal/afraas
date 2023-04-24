from django.db import models
from user.models import *

# Create your models here.
class Attendance(models.Model):
    time_stamp = models.DateTimeField()
    STATUS_CHOICES = [
    ("enter", "enter"),
    ("exit", "exit"),
    ("absent", "absent"),
    ]
    status = models.CharField(default="enter", max_length=50, choices=STATUS_CHOICES)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.id} | {self.user.name} - {self.time_stamp.day}/{self.time_stamp.month}/{self.time_stamp.year} - {self.status}"
    