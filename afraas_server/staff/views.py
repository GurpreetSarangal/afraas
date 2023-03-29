from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def dashboard(request):
    return HttpResponse("this is staff dashboard")

def users(request):
    return HttpResponse("this is users")

def other_tables(request):
    return HttpResponse("these are other tables")