from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return HttpResponse("admin dashboard")

def users(request):
    return HttpResponse("all users")

def other_tables(request):
    return HttpResponse("other tables")

def attendance(request):
    return HttpResponse("attendances table")