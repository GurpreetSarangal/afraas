from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path("mark/", views.mark, name="mark"),
    path("check_registered/", views.check_registered, name="check_registered"),
    path("report/", views.report, name="report"),
    path("add_user/", views.add_user, name="add_user"),
    path("mark_absent/", views.mark_absent, name="mark_absent"),
    path("recent-absent/", views.recent_absent, name="recent-absent"),
    path("recent-entries/", views.recent_entries, name="recent-entries"),
]