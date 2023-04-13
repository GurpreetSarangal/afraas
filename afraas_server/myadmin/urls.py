from django.urls import path
from . import views

app_name = 'myadmin'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("users/", views.users),
    path("other-tables/", views.other_tables),
    path("attendance/", views.attendance),
]