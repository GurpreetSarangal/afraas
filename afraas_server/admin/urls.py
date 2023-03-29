from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard),
    path("users/", views.users),
    path("other-tables/", views.other_tables),
    path("attendance/", views.attendance),
]