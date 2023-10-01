from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("users/", views.users, name="users"),
    path("departments/", views.departments, name="departments"),
    path("shifts/", views.shifts, name="shifts"),
    path("attendance/", views.attendance, name="attendance"),
]