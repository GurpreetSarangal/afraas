from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def dashboard(request):
    context = {
        "title" : "AFRAAS | Staff",
        "page" : "dashboard",
        "absentees" : [],
        "entries":[],
    }
    return render(request, "user/dashboard.html", context)

def apply_leave(request):
    return HttpResponse("apply leave here")

def profile(request):
    return HttpResponse("view you profile")

def profile_edit(request):
    return HttpResponse("edit your profile here")