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
    absentes = Attendance.objects.filter(status="absent").order_by("-time_stamp")
    filtered = absentes[0:3]

    for obj in filtered:
        time = str(obj.time_stamp.time())
        time = time.split(".")[0]
        date = str(obj.time_stamp.date()).split("-")
        

        temp = {
            "id" : obj.user.id,
            "name" : obj.user.name,
            "time_and_date": f"{date[2]}-{date[1]}-{date[0]} {time}"
        }
        context["absentees"].append(temp)

    entries = Attendance.objects.filter(status="enter").order_by("-time_stamp")
    filtered = entries[0:3]
    for obj in filtered:
        time = str(obj.time_stamp.time())
        time = time.split(".")[0]
        date = str(obj.time_stamp.date()).split("-")
        

        temp = {
            "id": obj.user.id,
            "name" : obj.user.name,
            "time_and_date": f"{date[2]}-{date[1]}-{date[0]} {time}"
        }
        context["entries"].append(temp)

    now = datetime.datetime.now()

    entries = Attendance.objects.filter(status="enter", time_stamp__date=now.date())
    all_users = User.objects.all()
    percent = (len(entries) / len(all_users))*100

    print(percent)
    print(len(entries), len(all_users))
    

    context["attendance_today_percent"] = percent
    context["total_present"] = len(entries)
    context["total_users"] = len(all_users)
    context["attendance_today_meter"] = 190-(190*(percent/100))

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    entries = Attendance.objects.filter(status="enter", time_stamp__date=yesterday)
    all_users = User.objects.all()
    percent = (len(entries) / len(all_users))*100

    context["attendance_yest_percent"] = percent
    context["yest_present"] = len(entries)
    context["yest_users"] = len(all_users)
    context["attendance_yest_meter"] = 190-(190*(percent/100))
    print(percent)
    print(len(entries), len(all_users))

    return render(request, "staff/dashboard.html", context)

def users(request):
    context = {
        "title" : "Users | Staff",
        "page" : "users",
        "content":[]
    }
    all_users = User.objects.all().order_by("id")
    now = datetime.datetime.now()
    for obj in all_users:
        status = ""
        st = Attendance.objects.filter(user=obj, time_stamp__date=now.date())
        if len(st) >= 1:
            if st[0].status == "absent":
                status = "Absent"
            else:
                if st[0].time_stamp.time() < obj.shift.time_in:
                    status = "Present"
                else:
                    status = "Late"
        else:
            status = "Not Marked Yet"
        temp = {
            "is_superuser":obj.is_superuser,
            "is_staff":obj.is_staff,
            "name": obj.name,
            "email": obj.email,
            "department": obj.department.name,
            "timings": f"{obj.shift.time_in} {obj.shift.time_out}",
            "status": status,
        }
        context["content"].append(temp)
    return render(request, "staff/users.html", context)

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