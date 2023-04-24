from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('apply-leave/', views.apply_leave, name="leave"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit', views.profile_edit, name="profile-edit"),
    
]