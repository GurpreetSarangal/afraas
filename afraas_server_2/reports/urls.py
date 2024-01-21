from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path("add_user/", views.add_user, name="add_user"),
    path("delete_user/", views.delete_user, name="delete_user"),

    path("reports/", views.report, name="reports"),
    path("recent-entries/", views.recent_entries, name="recent-entries"),
    path("recent-absent/", views.recent_absent, name="recent-absent"),

    path("check_registered/", views.check_registered, name="check_registered"),
    path("mark/", views.mark, name="mark"),
    path("mark_absent/", views.mark_absent, name="mark_absent"),
    path("mark_present/", views.mark_present, name="mark_present"),
    path("mark_left/", views.mark_left, name="mark_left"),
    path("mark_face_registered/", views.mark_face_registered, name="mark_face_registered"),
    path("mark_face_unregistered/", views.mark_face_unregistered, name="mark_face_unregistered"),
    path("check_image_input/", views.checkImageInput, name="check"),
    path("remote_image/", views.remote_image, name="remote_image"),

]