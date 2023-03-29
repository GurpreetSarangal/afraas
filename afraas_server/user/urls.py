from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('apply-leave/', views.apply_leave),
    path('profile/', views.profile),
    path('profile/edit', views.profile_edit),
    
]