from django.shortcuts import render
from django.http import HttpResponse
import datetime
from datetime import  date, time, timedelta
from user.models import *
from reports.models import *
import pytz
import calendar

# Create your views here.
def dashboard(request):
    context = {
        "title" : "AFRAAS | User",
        "page" : "dashboard",
        "working_day_digits":[0],
        "on_time_digits":[0],
        "late_digits":[0],
        "leave_digits":[0],
        "absent_digits":[0],
        "chart_data": [],
    }
    now = datetime.datetime.now()

    working_days = 0
    present = 0
    late_days = 0
    absent = 0
    leave = 0

    att = Attendance.objects.filter(user=request.user, time_stamp__month=now.month, time_stamp__year=now.year)
    working_days = len(att)
    for obj in att:
        if obj.status == "enter":
            dt = datetime.datetime.combine(date.today(), request.user.shift.time_in) + timedelta(minutes=30)
            if obj.time_stamp.time() <= dt.time():
                present += 1
            else:
                late_days += 1
        elif obj.status == "exit":
            pass
        elif obj.status == "absent":
            leave += 1
        else:
            absent += 1

    while(working_days > 0):
        dig = working_days % 10
        working_days = working_days // 10
        context["working_day_digits"].append(dig)
    while(present >0):
        dig = present % 10
        present = present // 10
        context["on_time_digits"].append(dig)
    while(late_days > 0):
        dig = late_days % 10
        late_days = late_days // 10
        context["late_digits"].append(dig)
    while(absent > 0):
        dig = absent % 10
        absent = absent // 10
        context["absent_digits"].append(dig)
    while(leave > 0):
        dig = leave % 10
        leave = leave // 10
        context["leave_digits"].append(dig)

    context["chart_data"] ={
        "month": now.strftime("%B"),
        "year": str(now.year),
        "data" : []
    }

    context["chart_data"]["data"]= monthly_on_daily_basis(request.user.id)


    return render(request, "user/dashboard.html", context)

def monthly_on_daily_basis(user_id):
    now = datetime.datetime.now()
    
    data = []
    year = now.year
    month = now.month
    cal = calendar.monthcalendar(year, month)
    user = User.objects.get(id=user_id)
    
    # Iterate over each week
    for week in cal:
        # Iterate over each day in the week
        for day in week:
            # If the day is 0, it means it's a day from the previous or next month
            if day == 0:
                continue
            # Do something with the day
            time_in_array = [0,0,0]
            time_in = 0
            time_out_array = [0,0,0]
            time_out = 0
            
            
            shift_temp_out = user.shift.time_out
            shift_temp_out = str(shift_temp_out).split(":")
            hour= int(shift_temp_out[0])
            minutes = int(shift_temp_out[1])
            sec = int(shift_temp_out[2])
            shift_temp_out = [hour, minutes, sec]

            shift_temp_in = user.shift.time_in
            shift_temp_in = str(shift_temp_in).split(":")
            hour= int(shift_temp_in[0])
            minutes = int(shift_temp_in[1])
            sec = int(shift_temp_in[2])
            shift_temp_in = [hour, minutes, sec]

            # if day > now.day:
            if False:
                pass
            else:
                att = Attendance.objects.filter(time_stamp__day=day, time_stamp__month=month, time_stamp__year=year, user=user).order_by("time_stamp")
                
                # print(att)
                for obj in att:
                    print(obj)
                    if obj.status == "enter":
                        time_in = obj.time_stamp.time() 

                    elif obj.status == "exit":
                        time_out = obj.time_stamp.time()

                    
                        
                
                    

                if time_out == "00:00:00":
                    time_out = user.shift.time_out
            
            if time_in!=0:
                time_in = str(time_in).split(":")
                # print("time_in", time_in)
                hour= int(time_in[0])
                minutes = int(time_in[1])
                sec = int(time_in[2].split(".")[0])

                time_in_array = [hour,minutes,sec]
            else:
                time_in_array = [0, 0, 0]

            if time_out!=0:
                time_out = str(time_out).split(":")
                hour= int(time_out[0])
                minutes = int(time_out[1])
                sec = int(time_out[2].split(".")[0])
                time_out_array =[hour, minutes, sec]
            else:
                time_out_array=[0,0,0]

            

            

            temp = [
                day,
                time_in_array,
                time_out_array,
                shift_temp_out,
                shift_temp_in
            ]
            data.append(temp)


    return data

def apply_leave(request):
    return HttpResponse("apply leave here")

def profile(request):
    return HttpResponse("view you profile")

def profile_edit(request):
    return HttpResponse("edit your profile here")