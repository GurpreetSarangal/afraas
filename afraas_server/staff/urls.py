from django.urls import path
from . import views

app_name = "staff"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('users/', views.users),
    path('other-tables/', views.other_tables),
   
]