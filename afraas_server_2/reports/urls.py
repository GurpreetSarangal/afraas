from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path("add_user/", views.add_user, name="add_user"),

    path("reports/", views.report, name="reports"),
    path("recent-entries/", views.recent_entries, name="recent-entries"),
    path("recent-absent/", views.recent_absent, name="recent-absent"),

    path("check_registered/", views.check_registered, name="check_registered"),
    path("mark/", views.mark, name="mark"),
    path("mark_absent/", views.mark_absent, name="mark_absent"),
    path("mark_face_registered/", views.mark_face_registered, name="mark_face_registered"),
    path("mark_face_unregistered/", views.mark_face_unregistered, name="mark_face_unregistered"),

]