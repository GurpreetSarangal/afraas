from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    return HttpResponse("this is user dashboard")

def apply_leave(request):
    return HttpResponse("apply leave here")

def profile(request):
    return HttpResponse("view you profile")

def profile_edit(request):
    return HttpResponse("edit your profile here")