from django.shortcuts import render
from django.http import HttpResponse
import datetime
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
            "time_and_date": obj.time_stamp
        }
        context["absentees"].append(temp)

    entries = Attendance.objects.filter(status="enter").order_by("-id")
    filtered = entries[0:3]
    for obj in filtered:
        time = str(obj.time_stamp.time())
        time = time.split(".")[0]
        date = str(obj.time_stamp.date()).split("-")
        timestamp_str = str(obj.time_stamp)
        # print("timestr", timestamp_str)

        # convert to datetime object and localize to UTC timezone
        dt = datetime.datetime.fromisoformat(timestamp_str)
        # utc_timezone = pytz.timezone('UTC')
        # dt_utc = utc_timezone.localize(dt)
        # print(dt)

        # convert to Indian Standard Time (IST) timezone
        ist_timezone = pytz.timezone('Asia/Kolkata')
        dt_ist = dt.astimezone(ist_timezone)
        # print(dt_ist)

        dt = datetime.datetime.fromisoformat(timestamp_str)
        # format the datetime object to desired IST format with day and month name and AM/PM
        formatted_time = dt.strftime("%a %d %b %Y, %I:%M%p")
        # print("new ",formatted_time, "obj.user.id ", obj.user.id)
        
        
        temp = {
            "id": obj.user.id,
            "name" : obj.user.name,
            # "time_and_date": f"{date[2]}-{date[1]}-{date[0]} {time}"
            "time_and_date": obj.time_stamp
        }
        context["entries"].append(temp)

    now = datetime.datetime.now()

    entries = Attendance.objects.filter(status="enter", time_stamp__date=now.date())
    all_users = User.objects.all()
    percent = (len(entries) / len(all_users))*100

    # print(percent)
    # print(len(entries), len(all_users))
    

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
    # print(percent)
    # print(len(entries), len(all_users))

    entries = Attendance.objects.filter(status="enter", time_stamp__date=now.date())
    present = 0
    late = 0
    for obj in entries:
        if obj.time_stamp.time() < obj.user.shift.time_in:
            present += 1
        else:
            late += 1
    
    context["present_digits"] = []
    temp_present = present
    temp_late = late

    if present == 0:
        context["present_digits"].append(0)
    else:
        while(present > 0):
            dig = present%10
            present = present//10

            context["present_digits"].append(dig)
            print("pres dig - ", dig)
    
    context["late_digits"] = []
    print(temp_late)
    print(temp_present)
    if late == 0:
        context["late_digits"].append(0)
    else:
        while(late > 0):
            dig = late%10
            late = late//10

            context["late_digits"].append(dig)
            print("late dig - ", dig)
    
    absents = Attendance.objects.filter(status="absent", time_stamp__date=now.date())
    temp_absent = len(absents)
    absent = temp_absent
    context["absent_digits"] = []
    
    if absent == 0:
        context["absent_digits"].append(0)
    else:
        while(absent > 0):
            dig = absent%10
            absent = absent//10

            context["absent_digits"].append(dig)
            print("absent dig - ", dig)

    temp_not_marked = len(all_users) - (temp_present + temp_late + temp_absent)
    print(temp_not_marked)

    context["not_marked_digits"] = []
    not_marked = temp_not_marked
    if not_marked == 0:
        context["not_marked_digits"].append(0)
    else:
        while(not_marked > 0):
            dig = not_marked%10
            not_marked = not_marked//10

            context["not_marked_digits"].append(dig)
            print("not_marked dig - ", dig)
    

    # print(context["total_present"])   
    # print(context["present_digits"])
    # print(context["total_users"])
    # print(context["late_digits"])
    # context["absent_digits"] = [ 0, 3, 5]
    context["chart_data"] ={
        "month": now.strftime("%B"),
        "year": str(now.year),
        "data" : []
    } 
    context["chart_data"]["data"] = monthly_on_daily_basis()
    print(context["chart_data"])
    return render(request, "staff/dashboard.html", context) 

def monthly_on_daily_basis():
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
            at = Attendance.objects.filter(time_stamp__day=day, time_stamp__month=month, time_stamp__year=year)
            present = 0
            leave = 0
            late = 0
            for obj in at:
                if obj.status == "enter":
                    if obj.time_stamp.time() <= obj.user.shift.time_in:
                        present +=1 
                    else:
                        late+=1
                elif obj.status == "absent":
                    leave += 1
            
            absent = total_users - (present + leave + late)

            temp = [
                day,
                absent,
                leave,
                late,
                present
            ]
            data.append(temp)
            

                

            print(day,
                absent,
                leave,
                late,
                present)


    return data


def users(request):
    context = {
        "title" : "Users | Staff",
        "page" : "users",
        "content":[],
        "present_digits": [],
    }
    all_users = User.objects.all()
    now = datetime.datetime.now()
    for obj in all_users:
        status = ""
        print(obj)
        st = Attendance.objects.filter(user=obj, time_stamp__date=now.date()).order_by("-id")
        if len(st) >= 1:
            print(st[0])
            # print(st[1])
            if st[0].status == "exit":
                status = "Left the Premesis"

            elif st[0].status == "absent":
                status = "Absent"

            else:
                if st[0].time_stamp.time() < obj.shift.time_in:
                    status = "Present"
                else:
                    status = "Late"
        else:
            status = "Not Marked Yet"
        
        itself = "false"
        if request.user == obj:
            itself = "true"

        temp = {
            "id": obj.id,
            "itself": itself,
            "is_superuser":obj.is_superuser,
            "is_staff":obj.is_staff,
            "name": obj.name,
            "email": obj.email,
            "department": obj.department.name,
            "timings": {
                    "in": obj.shift.time_in,
                    "out": obj.shift.time_out,
            },
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