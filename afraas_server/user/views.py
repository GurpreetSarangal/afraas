from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import timedelta
from user.models import *
from reports.models import *
import pytz
import calendar

# Create your views here.
def dashboard(request):
    context = {
        "title" : "AFRAAS | Staff",
        "page" : "dashboard",
        "absentees" : [],
        "entries":[],
        "chart_data": [],
    }

    context["chart_data"]= monthly_on_daily_basis(request.user)


    return render(request, "user/dashboard.html", context)

def monthly_on_daily_basis(user):
    now = datetime.datetime.now()
    # at = Attendance.objects.filter(time_stamp__month = now.month, time_stamp__year = now.year).order_by("time_stamp__day")
    # print(at)
    data = []
    year = now.year
    month = now.month
    cal = calendar.monthcalendar(year, month)
    total_users = len(User.objects.all())

    # Iterate over each week
    for week in cal:
        # Iterate over each day in the week
        for day in week:
            # If the day is 0, it means it's a day from the previous or next month
            if day == 0:
                continue
            # Do something with the day
            time_in = 0
            time_out = 0
            marked_leave = 0
            absent = 0
            if day > now.day:
                pass
            else:
                at = Attendance.objects.filter(time_stamp__day=day, time_stamp__month=month, time_stamp__year=year, user=user).order_by("time_stamp")
                
                for obj in at:
                    if obj.status == "enter":
                        time_in = obj.time_stamp.time() 

                    elif obj.status == "exit":
                        time_out = obj.time_stamp.time()

                    elif obj.status == "absent":
                        marked_leave = obj.time_stamp.time()
                        
                if time_in == 0 and marked_leave == 0:
                    d1 = datetime.datetime(2000, 1, 1, user.shift.time_in.hour, user.shift.time_in.minute, user.shift.time_in.second)
                    d2 = d1 + timedelta(hours=1, minutes=23)
                    absent = d2.time()
                    # absent = user.shift.time_in + timedelta(minutes=30)
                    

                elif time_out == 0:
                    time_out = user.shift.time_out()

            temp = [
                day,
                time_in,
                time_out,
                marked_leave,
                absent,
                user.shift.time_out
            ]
            data.append(temp)
            

                

            print(day,
                time_in,
                time_out,
                marked_leave,
                absent,
                user.shift.time_out)


    return data

def apply_leave(request):
    return HttpResponse("apply leave here")

def profile(request):
    return HttpResponse("view you profile")

def profile_edit(request):
    return HttpResponse("edit your profile here")