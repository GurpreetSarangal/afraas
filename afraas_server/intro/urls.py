
# from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # path('django-admin/', admin.site.urls),
    path("", views.landingPage, name="home"),
    path("login/", views.login, name="login"),
    path("help/", views.help, name="help"),
    path("developer-support/", views.developer_support, name="developer-support"),
    path("credits/", views.credits, name="credits"),
    path("contact-us/", views.contact_us, name="contact-us"),
    path("about-us/", views.about_us, name="about-us"),
    path("report-issue/", views.report_issue, name="report-issue"),
]
