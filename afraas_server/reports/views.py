from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import *
from .models import *
from django.db.models.functions import ExtractWeek
import json
import datetime
from datetime import date, timedelta
from django.db.models import Q
from pytz import timezone
import pytz

# Create your views here.
@csrf_exempt
def mark(request):
    if request.method == "POST":
        res = {
                "content" : "",
                "error" : "",
                "success": False,

        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # print("the request is ajax")
            data = json.loads(request.body.decode('utf-8'))
            label = data.get('label')
            st = data.get('status')
            timestamp = str(data.get('timestamp'))
            # date_string = timestamp.split(".")[0]
            print(" original ", timestamp)
            # Parse the string with a custom format string
        else:
            label = request.POST["label"]
            st = request.POST["status"]
            
        # now = datetime.datetime.now()
        time = datetime.datetime.now()
        label = label.split('_')[1]
        
        
        


        u = User.objects.filter(id=label[0])

        if len(u) == 0:
            res["error"] = "No user - rejected"
            json_data = json.dumps(res)
            return HttpResponse(json_data, content_type="application/json")

        check = Attendance.objects.filter(user=u[0], time_stamp__year=time.year, time_stamp__month=time.month, time_stamp__day=time.day, status="absent")
        if len(check) >= 1:
            res["error"] = "already marked absent rejected"
            json_data = json.dumps(res)
            return HttpResponse(json_data, content_type="application/json")

        if st == "exit":
            check = Attendance.objects.filter(user=u[0], time_stamp__year=time.year, time_stamp__month=time.month, time_stamp__day=time.day, status="enter")
            if len(check)==0:
                res["error"] = "to exit first enter the user"
                json_data = json.dumps(res)
                return HttpResponse(json_data, content_type="application/json")

        if st=="absent":
            check = Attendance.objects.filter(user=u[0], time_stamp__year=time.year, time_stamp__month=time.month, time_stamp__day=time.day, status="exit")
            if len(check)==1:
                res["error"] = "user has already left the office after work"
                json_data = json.dumps(res)
                return HttpResponse(json_data, content_type="application/json")

            check = Attendance.objects.filter(user=u[0], time_stamp__year=time.year, time_stamp__month=time.month, time_stamp__day=time.day, status="enter")
            if len(check)==1:
                res["error"] = "user already in the office"
                json_data = json.dumps(res)
                return HttpResponse(json_data, content_type="application/json")


        check = Attendance.objects.filter(user=u[0], time_stamp__year=time.year, time_stamp__month=time.month, time_stamp__day=time.day, status=st)
        if len(check) == 1:
            res["error"] = "same status already marked rejected"
            json_data = json.dumps(res)
            return HttpResponse(json_data, content_type="application/json")
        
        

        att = Attendance(status=st, user=u[0], time_stamp = time)  
        att.save()
        res["content"] = "accepted"+str(time)
        res["success"] = True
        json_data = json.dumps(res)
        return HttpResponse(json_data, content_type="application/json")
    else:
        return HttpResponse("not a post request")

@csrf_exempt
def check_registered(request):
    if request.method == "POST":
        id = request.POST['id']
        u = User.objects.filter(id=id)
        res = {
            "error" : "",
            "content" : [],
        }
        if len(u) == 0:
            res["error"] = "rejected"
            json_data = json.dumps(res)
            return HttpResponse(json_data, content_type="application/json")
           
        
        
        
        else:
            res["content"] = u[0].name
            json_data = json.dumps(res)
            return HttpResponse(json_data, content_type="application/json")
            
    
    return HttpResponse("Not a post request")

@csrf_exempt
def report(request):
    if request.method == "POST":
        type_of_report = request.POST['type']
        time = request.POST['time']

        if type_of_report == "user":
            # print(request.POST["u_id"])
            json_data = get_user(time, request.POST["u_id"])
            json_data = json.dumps(json_data)
            return HttpResponse(json_data, content_type="application/json") 

        elif type_of_report == "department":
            json_data = get_dept(time, request.POST["dept_id"])
            json_data = json.dumps(json_data)
            return HttpResponse(json_data, content_type="application/json") 

        elif type_of_report == "organization":
            return HttpResponse()
        else:
            return HttpResponse()
    else:
        return HttpResponse("not a post request")

def get_user( time, u_id):
    u = User.objects.get(id=u_id)
    res = {
            "heading" : [],
            "content" : [],
            "error" : "",

    }

    if time == "daily":
        now = datetime.datetime.now()
        res = {
            "heading" : ["Date", "In Time", "Out Time", "Shift", "Leave"],
            "content" : [],
            "error" : "",

        }
        try:
            att_check = Attendance.objects.get(time_stamp__year=now.year, time_stamp__month=now.month, time_stamp__day=now.day, user__id=u.id, status="absent")
            print(att_check)
            res["content"].append( [
                f"{now.day}/{now.month}/{now.year}",
                "-",
                "-",
                f"{u.shift.time_in.hour}-{u.shift.time_in.minute} to {u.shift.time_out.hour}-{u.shift.time_out.minute}",
                "yes",
            ] )
        except:

            att_enter = Attendance.objects.filter(time_stamp__year=now.year, time_stamp__month=now.month, time_stamp__day=now.day, user__id=u.id, status="enter")

            att_exit = Attendance.objects.filter(time_stamp__year=now.year, time_stamp__month=now.month, time_stamp__day=now.day, user__id=u.id, status="exit")
            if len(att_exit)==0:
                res["content" ].append([
                    f"{now.day}/{now.month}/{now.year}",
                    f"{att_enter[0].time_stamp.hour}-{att_enter[0].time_stamp.minute}",
                    # f"{att_exit[0].time_stamp.hour}-{att_enter[0].time_stamp.minute}",
                    f"-",
                    f"{u.shift.time_in.hour}-{u.shift.time_in.minute} to {u.shift.time_out.hour}-{u.shift.time_out.minute}", 
                    f"-"               
                ])
            else:
                res["content" ].append([
                    f"{now.day}/{now.month}/{now.year}",
                    f"{att_enter[0].time_stamp.hour}-{att_enter[0].time_stamp.minute}",
                    f"{att_exit[0].time_stamp.hour}-{att_enter[0].time_stamp.minute}",
                    # f"-",
                    f"{u.shift.time_in.hour}-{u.shift.time_in.minute} to {u.shift.time_out.hour}-{u.shift.time_out.minute}", 
                    f"-"               
                ])
        return res

    elif time=="weekly":
        res["error"] = "weekly for user is not supported"
        return res
    
    # elif time=="monthly":
    #     now = datetime.datetime.now()

    #     filtered_objects = Attendance.objects.filter(time_stamp__month=now.month, time_stamp__year=now.year, user=u)

    #     time_in = u.shift.time_in
    #     grouped_objects = filtered_objects.annotate(week=ExtractWeek('time_stamp')).order_by('week')
        
    #     res = {
    #         "heading" : ["Week No", "Present Days", "Total Late", "Total Leave"],
    #         "content" : [],
    #         "error" : "",
    #     }

    #     present = late = absent = 0
    #     init_week = grouped_objects[0].week
    #     # print(grouped_objects)
    #     for obj in grouped_objects:
    #         # print(obj, obj.week)
    #         if obj.week == init_week:
    #             if obj.status == "enter":
    #                 if obj.time_stamp.time() <= time_in:
    #                     present += 1
    #                 else:
    #                     late +=1
    #             if obj.status == "absent":
    #                 absent += 1
    #         else:
    #             temp = [init_week, present, late, absent]
    #             res["content"].append(temp)
    #             present = late = absent = 0

    #             init_week = obj.week

    #             if obj.status == "enter":
    #                 if obj.time_stamp.time() <= time_in:
    #                     present += 1
    #                 else:
    #                     late +=1
    #             if obj.status == "absent":
    #                 absent += 1
            
    #     temp = [init_week, present, late, absent]
    #     res["content"].append(temp)
    #     # print(res)
    #     return res
    
    
    elif time=="yearly":
        res["error"] = "Yearly not supported yet"
        return res

def get_dept( time, dept_id):
    res = {
            "heading" : [],
            "content" : [],
            "error" : "",
    }

    if time=="daily":
        now = datetime.datetime.now()
        user_set = User.objects.filter(department__id=dept_id)
        if(len(user_set) == 0):
            res["error"] = "No User is listed in this Department"
            return res

        present = Attendance.objects.filter(user__department__id=dept_id, time_stamp__date=now.date(), status="enter")
        leave = Attendance.objects.filter(user__department__id=dept_id, time_stamp__date=now.date(), status="absent")

        absent = len(user_set) - len(present) - len(leave)


        res = {
            "heading" : ["Date", "No of Employee", "Present", "Absent", "Leave"],
            "content" : [
                f"{now.day}/{now.month}/{now.year}",
                f"{len(user_set)}",
                f"{len(present)}",
                f"{absent}",
                f"{len(leave)}",
            ],
        }
        return res
        
    
    elif time=="weekly":
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        user_set = User.objects.filter(department__id=dept_id)  

        
        if(len(user_set) == 0):
            res["error"] = "No User is listed in this Department"
            return res

        # filter records for the current week
        user_set_week = Attendance.objects.filter(
            Q(time_stamp__gte=start_of_week) &
            Q(time_stamp__lte=end_of_week),
            user__department__id=dept_id
        )

        present = Attendance.objects.filter(
            Q(time_stamp__gte=start_of_week) &
            Q(time_stamp__lte=end_of_week),
            user__department__id=dept_id,
            status="enter",
        )

        leave = Attendance.objects.filter(
            Q(time_stamp__gte=start_of_week) &
            Q(time_stamp__lte=end_of_week),
            user__department__id=dept_id,
            status="absent",
        )

        absent = len(user_set) - len(present) - len(leave)

        avg_attendance = ((len(user_set) - len(leave) - absent) / len(user_set)) * 100


        late_entries = 0
        for user in user_set_week:
            time_in = user.user.shift.time_in
            if user.time_stamp.time() > time_in:
                late_entries += 1 

        res = {
            "heading" : ["Week Start", "Week End", "No of Employees", "Total Present", "Total Absent", "Total Leave", "Total Late", "Avg Attendance"],
            "content" : [
                str(start_of_week),
                str(end_of_week),
                len(user_set),
                absent,
                len(leave),
                late_entries,
                avg_attendance,
            ],
            "error" : "",           

        }
        return res

    # elif time=="monthly":
    #     now = datetime.datetime.now()

    #     filtered_objects = Attendance.objects.filter(time_stamp__month=now.month, time_stamp__year=now.year, user__department__id=dept_id)

    #     grouped_objects = filtered_objects.annotate(week=ExtractWeek('time_stamp')).order_by('week')

    #     res = {
    #         "heading" : ["Week No", "No of Employees", "Present", "Absent", "Leave", "Average Attendace"],
    #         "content": [],
    #         "error" : "",
            
    #     }

    #     emp = len(User.objects.filter(department__id=dept_id))

    #     present = absent = leave = avg_attendance = 0
    #     try:
    #         init_week = grouped_objects[0].week
    #     except:
    #         res["error"] = "No User is listed in this Department"
    #         return res

    #     for obj in grouped_objects:
    #         if obj.week == init_week:
    #             # print(obj, obj.week)
    #             if obj.status == "enter":
    #                 present +=1
    #                 # print("Present = ", present, "status = ", obj.status)
    #             elif obj.status == "absent":
    #                 leave +=1
    #                 # print("Leave = ", leave, "status = ", obj.status)
    #         else:
    #             absent = (emp*7) - (present + leave)
    #             avg_attendance = (present / (emp*7))*100
    #             temp = [
    #                 init_week,
    #                 emp,
    #                 present,
    #                 absent,
    #                 leave,
    #                 avg_attendance,
    #             ]
    #             # print(temp)
    #             res["content"].append(temp)
    #             init_week = obj.week
    #             present = absent = leave = avg_attendance = 0
                
                
    #     absent = emp - present - leave
    #     avg_attendance = (present / emp)*100
    #     temp = [
    #         init_week,
    #         emp,
    #         present,
    #         absent,
    #         leave,
    #         avg_attendance,
    #     ]
    #     res["content"].append(temp)
    #     # print(res)
    #     return res
    
    elif time=="yearly":
        pass
    
    else:

        pass

def get_org(request, time):
    pass

@csrf_exempt
def recent_absent(request):
    context = {
        "error":"",
        "content": [],
        "success":True,
    }
    if request.method == "POST":
        max_len = 3
        # print(request.GET)
        a = Attendance.objects.filter(status="absent").order_by("-time_stamp")[0:max_len]

        for obj in a:
            time = str(obj.time_stamp.time())
            time = time.split(".")[0]
            date = str(obj.time_stamp.date()).split("-")

            # input timestamp in string format
            timestamp_str = str(obj.time_stamp)

            # convert to datetime object and localize to UTC timezone
            dt = datetime.datetime.fromisoformat(timestamp_str)
            # utc_timezone = pytz.timezone('UTC')
            # dt_utc = utc_timezone.localize(dt)

            # convert to Indian Standard Time (IST) timezone
            ist_timezone = pytz.timezone('UTC')
            dt_ist = dt.astimezone(ist_timezone)

            # format the datetime object to desired IST format with day and month name and AM/PM
            formatted_time = dt_ist.strftime("%a %d %b %Y, %I:%M%p")
            print(formatted_time)

            temp = {
                "id": obj.user.id,
                "name" : obj.user.name,
                "time_and_date": formatted_time
            }
            context["content"].append(temp)
        json_data = context
        json_data = json.dumps(json_data)
        return HttpResponse(json_data, content_type="application/json")
        
    else:
        return HttpResponse("not a post request")
    
@csrf_exempt
def recent_entries(request):
    context = {
        "error":"",
        "content": [],
        "success":True,
    }
    if request.method=='POST':
        try:
            a = Attendance.objects.filter(status="enter").order_by("-time_stamp")[0:3]
        except:
            context["success"] = False
            json_data = context
            json_data = json.dumps(json_data)
            return HttpResponse(json_data, content_type="application/json")
        for obj in a:
            time = str(obj.time_stamp.time())
            time = time.split(".")[0]
            date = str(obj.time_stamp.date()).split("-")
            
            print(obj.time_stamp.strftime('%a %d %b %Y, %I:%M%p'))
            temp = {
                "id": obj.user.id,
                "name" : obj.user.name,
                "time_and_date": obj.time_stamp.strftime('%a %d %b %Y, %I:%M%p'),
            }

            context["content"].append(temp)
        
        json_data = context
        json_data = json.dumps(json_data)
        return HttpResponse(json_data, content_type="application/json")
        
    else:
        return HttpResponse()


@csrf_exempt
def add_user(request):
    res = {
            "error" : '',
            "success": False,
    }

    if request.method == "POST" and request.user.is_staff:
        
        name = request.POST["name"]
        email = request.POST["email"]
        shift = request.POST["shift"]
        department = request.POST["department"]
        psw = request.POST["new_password"]
        confirm_psw = request.POST["confirm_new_password"]
        type_of_user = request.POST["type_of_user"]
        is_unique_mail = True
        print(name)
        print(email)
        print(shift)
        print(department)
        print(psw)
        print(confirm_psw)
        print(type_of_user)

        if not request.user.is_superuser and type_of_user!="gen_user":
            res["error"] = "A Staff member is not allowed to create "+type_of_user+" type of users"
        
        else:

            all_users = User.objects.all().order_by("id")
            for obj in all_users:
                print(obj)
                if email == obj.email:
                    is_unique_mail = False
                    break
            
            if not is_unique_mail:
                res["error"] = f"Email [{email}] is already registred"
            
            if not psw==confirm_psw:
                res["error"]= "Passwords are not same. Try Again"

            else:
                res["success"] = True
            try:
                dept = Department.objects.get(id=department)
                sh = Shift.objects.get(id=shift)
                
                if type_of_user == "gen_user":
                    u = User.objects.create_user(
                        email= email,
                        
                        password= psw,
                        name= name,
                        department=dept,
                        shift=sh,
                    )
                    u.save()

                elif type_of_user == "staff":
                    u = User.objects.create_staffuser(
                        email=email,
                        
                        password=psw,
                        name= name,
                        department=dept,
                        shift=sh,
                    )
                    u.save()

                elif type_of_user == "superuser":
                    u = User.objects.create_superuser(
                        email=email,
                        
                        password=psw,
                        name= name,
                        department=dept,
                        shift=sh,
                    )
                    u.save()
                
            except Exception as e:
                print(e)
                res["error"]= "There is some internal server error"
                res["success"] = False
       
    else:
        res["error"]="Either this is not a POST request Or You are not a authorized user"
    
    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")