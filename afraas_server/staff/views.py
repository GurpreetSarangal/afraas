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
    

    context["attendance_today_percent"] = truncate(percent,1) 
    context["total_present"] = len(entries)
    context["total_users"] = len(all_users)
    context["attendance_today_meter"] = truncate(190-(190*(percent/100)), 2)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    entries = Attendance.objects.filter(status="enter", time_stamp__date=yesterday)
    all_users = User.objects.all()
    percent = (len(entries) / len(all_users))*100

    context["attendance_yest_percent"] = truncate(percent,1) 
    context["yest_present"] = len(entries)
    context["yest_users"] = len(all_users)
    context["attendance_yest_meter"] = truncate(190-(190*(percent/100)), 2)
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

    context["all_users_digits"] = []
    all_users = context["total_users"]
    if all_users == 0:
        context["all_users_digits"].append(0)
    else:
        while(all_users > 0):
            dig = all_users%10
            all_users = all_users//10

            context["all_users_digits"].append(dig)
            print("all_users dig - ", dig)
    

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
            present = 0
            leave = 0
            late = 0
            absent = 0
            if day > now.day:
                pass
            else:
                at = Attendance.objects.filter(time_stamp__day=day, time_stamp__month=month, time_stamp__year=year)
                
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
                present,
                total_users
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
        "error" : "",
        "content":[],
        "present_digits": [],
        "all_departments": [],
        "all_shifts": [],
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
                status = "Leave"

            else:
                if st[0].time_stamp.time() <= obj.shift.time_in:
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
    # print(context["content"])

    

    dept = Department.objects.all().order_by("id")
    for obj in dept:
        temp={
            "id": obj.id,
            "name": obj.name,
        }

        context["all_departments"].append(temp)
    
    shift = Shift.objects.all().order_by("id")
    for obj in shift:
        name = ""
        if str(obj.time_in) == "07:00:00":
            name = "Morning"
        elif str(obj.time_in) == "15:00:00":
            name = "Afternoon"
        elif str(obj.time_in) == "23:00:00":
            name = "Night"

        temp = {
            "id": obj.id,
            "name": name,
            "time_in": obj.time_in,
            "time_out": obj.time_out,
        }
        context["all_shifts"].append(temp)

    return render(request, "staff/users.html", context)

def other_tables(request):
    context = {
        "title" : "Tables | Staff",
        "page" : "other-tables",
        "shift_table": [],
        "department_table": [],
    }

    all_shifts = Shift.objects.all().order_by("id")
    for obj in all_shifts:
        u = User.objects.filter(shift=obj)
        name = ""
        if str(obj.time_in) == "07:00:00":
            name = "Morning"
        elif str(obj.time_in) == "15:00:00":
            name = "Afternoon"
        elif str(obj.time_in) == "23:00:00":
            name = "Night"
        temp = {
            "id": obj.id,
            "name": name,
            "time_in": obj.time_in,
            "time_out": obj.time_out,
            "no_of_emp": len(u),
        }
        context["shift_table"].append(temp)
    
    all_depts = Department.objects.all().order_by("id")
    for obj in all_depts:
        u = User.objects.filter(department=obj)
        temp = {
            "id": obj.id,
            "name": obj.name,
            "no_of_emp": len(u),
        }
        context["department_table"].append(temp)


    return render(request, "staff/other_tables.html", context) 

 

def attendance(request):
    context = {
        "title" : "Attendance | Staff",
        "page" : "attendance",
        "content": [],
    }

    all_recs=Attendance.objects.all().order_by("-id")

    for obj in all_recs:
        itself = ""
        if request.user.id == obj.user.id:
            itself = "true"
        user_status = ""
        if obj.status=="exit":
            if obj.time_stamp.time() >= obj.user.shift.time_out:
                user_status="left after time"
            else:
                user_status="left before time"
        elif obj.status=="enter":
            if obj.time_stamp.time() <= obj.user.shift.time_in:
                user_status = "on time"
            else:
                user_status = "late"
        
        elif obj.status=="absent":
            user_status="on leave"

        temp = {
            "id": obj.id,
            "user" : {
                "id": obj.user.id,
                "name": obj.user.name,
                "email": obj.user.email,
                "is_superuser": obj.user.is_superuser,
                "is_staff": obj.user.is_staff,
                "itself": itself,
                "status": user_status,
                "time_in": obj.user.shift.time_in,
                "time_out": obj.user.shift.time_out,
            },
            "time_stamp": obj.time_stamp,
            "status": obj.status,

        }
        context["content"].append(temp)

    return render(request, "staff/attendance.html", context) 


def reports(request):
    context = {
        "title" : "Reports | Staff",
        "page" : "reports",
        "users_table_content":[],
        "department_table_content": [],
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
                status = "Leave"

            else:
                if st[0].time_stamp.time() <= obj.shift.time_in:
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
        context["users_table_content"].append(temp)

    all_depts = Department.objects.all().order_by("id")
    for obj in all_depts:
        u = User.objects.filter(department=obj)
        temp = {
            "id": obj.id,
            "name": obj.name,
            "no_of_emp": len(u),
        }
        context["department_table_content"].append(temp)

    # print(context["content"])
    return render(request, "staff/reports.html", context)

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])