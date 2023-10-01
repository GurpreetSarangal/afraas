from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('apply_leave/', views.apply_leave, name="apply_leave"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit', views.profile_edit, name="profile_edit"),
    path('yearly-data/', views.profile_edit, name="yearly_data"),
    
]