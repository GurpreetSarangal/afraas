from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('users/', views.users, name="users"),
    path('other-tables/', views.other_tables, name="other-tables"),
    path('attendance/', views.attendance, name="attendance"),
    path('reports/', views.reports, name="reports"),
    path('test/', views.test_new_user, name="test"),
   
]