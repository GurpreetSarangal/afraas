from django.shortcuts import render
from django.http import HttpResponse

def landingPage(request):
    return render(request, "intro/landing_page.html")

def login(response):
    return HttpResponse("this is login page")

def help(response):
    return HttpResponse("this is help page")

def developer_support(response):
    return HttpResponse("this is developer support page")

def credits(response):
    return HttpResponse("this is credits page")

def contact_us(response):
    return HttpResponse("this is contact us page")

def report_issue(response):
    return HttpResponse("this is report issue page")

def about_us(response):
    return HttpResponse("this is about us page")