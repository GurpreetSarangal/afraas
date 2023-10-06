# from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    
    path("", views.landingPage, name="home"),
    path("accounts/login/", views._login, name="login"),
    path("logout/", views._logout, name="logout"),
    path("help/", views.help, name="help"),
    path("developer-support/", views.developer_support, name="developer-support"),
    path("credits/", views.credits, name="credits"),
    path("contact-us/", views.contact_us, name="contact-us"),
    path("about-us/", views.about_us, name="about-us"),
    path("report-issue/", views.report_issue, name="report-issue"),
    
]
