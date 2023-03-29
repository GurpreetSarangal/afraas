"""afraas_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path("admin/", include("admin.urls")),
    path("staff/", include("staff.urls")),
    path("user/", include("user.urls")),
]
