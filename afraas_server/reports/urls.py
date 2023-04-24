from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path("mark/", views.mark, name="mark"),
    path("check_registered/", views.check_registered, name="check_registered"),
    path("report/", views.report, name="report"),
]