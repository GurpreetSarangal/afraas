from django.shortcuts import render
from django.http import HttpResponse
import datetime
from user.models import *
from reports.models import *

# Create your views here.
def dashboard(request):
    context = {
        "title" : "AFRAAS | Staff",
        "page" : "dashboard",
        "absentees" : [],
        "entries":[],
    }
    now = datetime.datetime.now()
    absentes = Attendance.objects.filter(status="absent").order_by("-time_stamp")[0:3]
    for obj in absentes:
        time = str(obj.time_stamp.time())
        time = time.split(".")[0]
        date = str(obj.time_stamp.date()).split("-")
        

        temp = {
            "name" : obj.user.name,
            "time_and_date": f"{date[2]}-{date[1]}-{date[0]} {time}"
        }
        context["absentees"].append(temp)

    entries = Attendance.objects.filter(status="enter").order_by("-time_stamp")[0:3]
    for obj in entries:
        time = str(obj.time_stamp.time())
        time = time.split(".")[0]
        date = str(obj.time_stamp.date()).split("-")
        

        temp = {
            "name" : obj.user.name,
            "time_and_date": f"{date[2]}-{date[1]}-{date[0]} {time}"
        }
        context["entries"].append(temp)


    return render(request, "staff/dashboard.html", context)

def users(request):
    context = {
        "title" : "Users | Staff",
        "page" : "users",
    }
    return HttpResponse("this is users")

def other_tables(request):
    context = {
        "title" : "Tables | Staff",
        "page" : "other-tables",
    }


    return HttpResponse("these are other tables")

def attendance(request):
    context = {
        "title" : "Attendance | Staff",
        "page" : "attendance",
    }
    return HttpResponse("attendance table")

def reports(request):
    context = {
        "title" : "Attendance | Staff",
        "page" : "reports",
    }
    return HttpResponse("reports")