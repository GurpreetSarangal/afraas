from django.shortcuts import render
from django.http import HttpResponse

def landingPage(request):
    context={
        "title": "Welcome | AFRAAS"
    }
    return render(request, "intro/landing_page.html", context)

def login(request):
    context={
        "title": "Login | AFRAAS"
    }
    return render(request, "intro/login.html", context)

def help(request):
    return HttpResponse("this is help page")

def developer_support(request):
    return HttpResponse("this is developer support page")

def credits(request):
    return HttpResponse("this is credits page")

def contact_us(request):
    return HttpResponse("this is contact us page")

def report_issue(request):
    return HttpResponse("this is report issue page")

def about_us(request):
    return HttpResponse("this is about us page")