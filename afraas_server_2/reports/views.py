from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import *
from user.manager import *
from .models import *
from .test import test
import pickle
import os.path
import datetime


import json
import datetime
import face_recognition

import pytz
import calendar
import numpy as np
from urllib.request import urlopen
import cv2
import base64

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
        print(label)
        label = label.split('_')[1]
        print(label)
        
        
        


        u = User.objects.filter(id=label)

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
    res = {
            "error" : "",
            "content" : [],
            "success": False,
        }
    if request.method == "POST":
        id = request.POST['id']
        u = User.objects.filter(id=id)
        
        if len(u) == 0:
            res["error"] = f"Not a valid id #{id}"        
              
        else:
            user = u[0]
            if user.is_registered ==  True:
                res["error"] = f"User #{user.id} {user.name} is already registered"
            else:
                res["success"] = True
                res["content"] = u[0].name
            
    else:
        res["error"]= "Not a post request"


    json_data = json.dumps(res)
    return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def report(request):
    res = {
        "error" : "",
        "success": False,
        "content" : [],
    }
    if request.user.is_staff:

        if request.method == "POST":
            type_of_report = request.POST['type']
            time = request.POST['time']



            if type_of_report == "user":
                # print(request.POST["u_id"])
                if time not in ["daily", "monthly"]:
                    res["error"]="Unsupported Time Period"
                else:
                    
                    try:
                        u_id = int(request.POST['id'])   
                        res["content"] = get_user(time, u_id)
                        res["success"] = True
                    except:
                        res["error"] = "No User is selected"
                        res["success"]=False
                    
                 

            elif type_of_report == "dept":
                if time not in ["daily",  "monthly"]:
                    res["error"] = "Unsupported Time Period"
                else:
                    try:
                        dept_id = int(request.POST["id"])
                    except:
                        res["error"]= "department was not selected"
                        res["success"] = False
                    
                    users = User.objects.filter(department__id=request.POST["id"])
                    if len(users)>0:
                        res["content"] = get_dept(time, request.POST["id"])
                        res["success"] = True
                    else:
                        res["error"] = "No user is listed in Department"
                        
                

            elif type_of_report == "org":
                if time not in ["daily","monthly"]:
                    res["error"] = "Unsupported Time Period"
                else:
                    res["content"] = get_org(time)
                    res["success"] = True
                    # res["error"]="Reports for Organization are under development right now."
                
            else:
                res["error"]="Unsupported type of report"
                return HttpResponse()
        else:
            res["error"]="Not a post request"
            
    else:
        res["error"]="You are not authorized"
    json_data = json.dumps(
                    res,
                    sort_keys=True,
                    indent=1,
                    default=default
                )
    return HttpResponse(json_data, content_type="application/json")

        

def get_user( time, u_id):
    u = User.objects.get(id=u_id)
    res = {
        "heading" : [],
        "data" : [],
    }

    if time == "daily":
        res = get_user_daily(u)    
    
    elif time=="monthly":
        res = get_user_monthly(u)

    
    
    elif time=="yearly":
        res = "Yearly not supported yet"
    
    return res

def get_dept(time, dept_id):


    if time=="daily":
        return get_dept_daily(dept_id)
                
        
    
    elif time=="weekly":
       pass

    elif time=="monthly":
        return get_dept_monthly(dept_id)
    
    elif time=="yearly":
        pass
    

def get_org(time):
    if time=="daily":
        return get_org_daily()
    if time=="monthly":
        return get_org_monthly()
    

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
def delete_user(request):
    res = {
            "error" : '',
            "success": False,
    }
    db_path = r"C:\Users\gurpr\Documents\_StudyMaterial\code\afraas\afraas_server_2\reports\static\reports\faceData"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        
        if request.method == "POST" and request.user.is_staff:
            
            data = json.loads(request.body)
            print(data["label"])

            uid = int(data["label"].split("_")[1])

            if uid != request.user.id:


                for i in range(1, 4):
                    file_path = db_path + "\\" + str(uid) + "_" + str(i) + ".pickle"
                    print(file_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    else:
                        print("File not found. "+file_path)
                        res["error"] = "There is some internal db error"
                        break

                
                if res["error"] == '':
                    temp_user = User.objects.get(id=uid);
                    # print(temp_user)
                    temp_user.delete()
                    res["success"] = True
            else:
                res["error"] = "Current user cannot be deleted."
           
    else:
        res["error"]="Either this is not a POST request Or You are not a authorized user"
    
    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")


@csrf_exempt
def add_user(request):
    res = {
            "error" : '',
            "success": False,
    }
    # print("This runs")
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # print("the request is ajax")
        if request.method == "POST" and request.user.is_staff:
            data = json.loads(request.body)
            
            # print(type(data))

            name = data["name"]
            email = data["email"]
            shift = data["shift"]
            department = data["department"]
            psw = data["new_password"]

            confirm_psw = data["confirm_new_password"]
            # img1 = data["img1"]
            # img2 = data["img2"]
            # img3 = data["img3"]
            type_of_user = data["type_of_user"]
            is_unique_mail = True
            print(name)
            print(email)
            print(shift)
            print(department)
            print(psw)
            # print(img1)
            # print(img2)
            # print(img3)
            print(confirm_psw)

            print(type_of_user)

            if not request.user.is_superuser and type_of_user!="gen_user":
                res["error"] = "A Staff member is not allowed to create "+type_of_user+" type of users"
            
            else:

                if not psw==confirm_psw:
                    res["error"]= "Passwords are not same. Try Again"

                else:

                    all_users = User.objects.all().order_by("id")
                    for obj in all_users:
                        print(obj)
                        print(email+" "+obj.email+" ", end="")
                        print(email==obj.email)

                        if email == obj.email:
                            is_unique_mail = False
                            break
                    
                    if not is_unique_mail:
                        res["error"] = f"Email [{email}] is already registred"

                    else:        
                        result_face_check, error, spoof_result = spoof_check(data)

                        if not result_face_check:   
                            res["error"] = error
                            res["spoof_result"] = spoof_result

                        else:
                            res["success"] = True
                            u = None
                            try:
                                dept = Department.objects.get(id=department)
                                sh = Shift.objects.get(id=shift)
                                
                                if type_of_user == "gen_user":
                                    u = User.objects.create_user(
                                        email= email,
                                        is_registered =  True,
                                        password= psw,
                                        name= name,
                                        department=dept,
                                        shift=sh,
                                    )
                                    # u.save()

                                elif type_of_user == "staff":
                                    u = User.objects.create_staffuser(
                                        email=email,
                                        is_registered =  True,
                                        password=psw,
                                        name= name,
                                        department=dept,
                                        shift=sh,
                                    )
                                    # u.save()

                                elif type_of_user == "superuser":
                                    u = User.objects.create_superuser(
                                        email=email,
                                        is_registered =  True,
                                        password=psw,
                                        name= name,
                                        department=dept,
                                        shift=sh,
                                    )
                                    # u.save()
                                
                            except Exception as e:
                                print(e)
                                res["error"]= "There is some internal server error"
                                res["success"] = False
                            
                            try:
                                if u is not None:
                                    data["id"] = User.objects.get(email=data["email"]).id
                                    print(data["id"])
                                    issaved, error = save_face(data)
                            
                            except Exception as e:
                                print(e)
        
    else:
        res["error"]="Either this is not a POST request Or You are not a authorized user"
    
    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")

def save_face(data):
    output_path = r'''C:\\Users\\gurpr\\Documents\\_StudyMaterial\\code\\afraas\\afraas_server_2\\reports\\static\\reports\\faceData\\'''
    temp_img1 = url_to_image(data["img1"].split(",")[1])
    temp_img2 = url_to_image(data["img2"].split(",")[1])
    temp_img3 = url_to_image(data["img3"].split(",")[1])


    embeddings1 = face_recognition.face_encodings(temp_img1)[0]
    name = str(data["id"])+"_1"
    file = open(os.path.join(output_path, '{}.pickle'.format(name)), 'wb')
    pickle.dump(embeddings1, file)

    embeddings2 = face_recognition.face_encodings(temp_img2)[0]
    file = open(os.path.join(output_path, '{}.pickle'.format(str(data["id"])+"_2")), 'wb')
    pickle.dump(embeddings2, file)

    embeddings3 = face_recognition.face_encodings(temp_img3)[0]
    file = open(os.path.join(output_path, '{}.pickle'.format(str(data["id"])+"_3")), 'wb')
    pickle.dump(embeddings3, file)

    return True, ""

def spoof_check(data):
    temp_img1 = url_to_image(data["img1"].split(",")[1])
    temp_img2 = url_to_image(data["img2"].split(",")[1])
    temp_img3 = url_to_image(data["img3"].split(",")[1])
    output_path = f'''C:\\Users\\gurpr\\Documents\\_StudyMaterial\\code\\afraas\\afraas_server_2\\reports\\static\\reports\\faceData\\'''
    model_dir = r'C:\Users\gurpr\Documents\_StudyMaterial\code\afraas\afraas_server_2\reports\resources\anti_spoof_models'
    first_checked = 1
    second_checked = 1
    third_checked = 1

    label_1 = test(
                image=temp_img1,
                model_dir=model_dir,
                device_id=0
            )
    
    if (label_1 != 1):
        print(label_1)
        first_checked = 0
        # return False, 'Image is not real'


    label_2 = test(
                image=temp_img2,
                model_dir=model_dir,
                device_id=0
            )
    if (label_2 != 1):
        print(label_2)
        second_checked = 0
        # return False, 'Image is not real'
    
    
    label_3 = test(
                image=temp_img3,
                model_dir=model_dir,
                device_id=0
            )
    
    if (label_3 != 1):
        print(label_3)
        third_checked = 0
        # return False, 'Image is not real'

    
    if first_checked and second_checked and third_checked:
        return True, '', [first_checked, second_checked, third_checked]
    else:
        return False, "Images needs to be re-captured" , [first_checked, second_checked, third_checked]



@csrf_exempt
def mark_absent(request):
    id = int(request.POST["id"])

    print(type(id))
    print(type(request.user.id))
    print(id, request.user.id)
    res = {
        "error": "",
        "success": False,
    }
    if request.method == "POST":
        if request.user.id == id:
            try:
                now = datetime.datetime.now()
                u = User.objects.get(id=id)
                ch = Attendance.objects.filter(user=u,
                time_stamp__date=now.date() ).order_by("-id")
                if len(ch)>0:
                    if ch[0].status == "exit":
                        res["error"]="You have already left the premesis"
                    elif ch[0].status == "enter":
                        res["error"] = "You are already in the office"
                    elif ch[0].status == "absent":
                        res["error"] = "You already marked on leave"
                else:

                    att = Attendance(
                        user=u,
                        time_stamp = datetime.datetime.now.time(),
                        status="absent",
                    )
                    att.save()
                    res["success"] = True
            except:
                res["error"] = "Not Marked due to internal error"
        else:
            res["error"] = "ID Sent and user logged in don't match"
    else:
        
        res["error"] = "Not a POST Request"
    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")

def get_user_daily(user, now = datetime.datetime.now()):
    res = {
        "title": "#"+str(user.id)+" "+user.name+"'s today's report",
        "heading": [
            "User",
            "Date",
            "Status",
            "Time In",
            "Time Out",
            "Shift Time In",
            "Shift Time Out",
        ],
        "data":[],
    }

    date = now.strftime("%a,%d %b, %Y")
    time_in = datetime.time(0)
    time_out = datetime.time(0)
    status = ""
    att = Attendance.objects.filter(user = user, time_stamp__date = now.date()).order_by("-id")
    print(att)
    if len(att) == 2:
        time_out = att[0].time_stamp.time()
        time_in = att[1].time_stamp.time()
        status = "left the premesis"
    elif len(att) == 1:
        status = att[0].status
        if status == "enter":
            time_in = att[0].time_stamp
        elif status == "absent":
            status = "on leave"
    elif len(att) == 0:
        status = "not marked yet"
    
    
    uname = "# "+str(user.id)+" "+user.name

    res["data"] = [
        [
            uname,
            date,
            status,
            time_in.strftime("%H.%M %p"),
            time_out.strftime("%H.%M %p"),
            user.shift.time_in.strftime("%H.%M %p"),
            user.shift.time_out.strftime("%H.%M %p")
        ]
    ]
    return res

def get_user_monthly(user):
    res = {
        "title": "#"+str(user.id)+" "+user.name+"'s monthly report",
        "heading": [
            "Week No",
            "Days On Time",
            "Days Late",
            "Days Leave",
            "Days Absent",
        ],
        "data": [],
    }
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    cal = calendar.monthcalendar(year, month)
    days_on_time_month = 0
    days_late_month = 0
    days_leave_month = 0
    days_absent_month = 0
    week_no = 0
    # Iterate over each week

    for week in cal:
        # Iterate over each day in the week
        week_no += 1
        days_on_time_week = 0
        days_late_week = 0
        days_leave_week = 0
        days_absent_week = 0

        for day in week:
            # If the day is 0, it means it's a day from the previous or next month

            if day == 0:
                continue
            # Do something with the day

            att = Attendance.objects.filter(
                time_stamp__day = day,
                time_stamp__month=month,
                time_stamp__year=year,
                user = user).order_by("-id")
            
            if len(att) == 2:
                if att[0].time_stamp.time() <= user.shift.time_in:
                    days_on_time_week +=1
                else:
                    
                    days_late_week +=1
                
            elif len(att) == 1:
                if att[0].status=="absent":
                    days_leave_week+=1
                else:
                    days_on_time_week +=1
            
            elif len(att) == 0:
                days_absent_week += 1

        days_on_time_month += days_on_time_week
        days_late_month += days_late_week
        days_leave_month += days_leave_week
        days_absent_month += days_absent_week

        temp = [
            week_no,
            days_on_time_week,
            days_late_week,
            days_leave_week,
            days_absent_week,
        ]
        res["data"].append(temp)

    temp = [
        "total",
        days_on_time_month,
        days_late_month,
        days_leave_month,
        days_absent_month,
    ]
    res["data"].append(temp)
    return res

def get_org_daily():
    res = {
        "title": "An organisational report on daily basis",
        "heading":[
            "Date",
            "User",
            "Dept",
            "Status",
            "Time In",
            "Time Out", 
            "Shift",
        ],
        "data" : [],
    }
    all_users = User.objects.all().order_by("id")
    for user in all_users:
        temp = get_user_daily(user)
        u_data = [
            temp["data"][0][1],
            temp["data"][0][0],
            user.department.name,
            temp["data"][0][2],
            temp["data"][0][3],
            temp["data"][0][4],
            temp["data"][0][5]+ " - "+temp["data"][0][6],            
        ]
        res["data"].append(u_data)
    return res


def get_org_monthly():
    res = {
        "title": "An organisational report for a month",
        "heading": [
            "User",
            "Dept",
            "On Time Days",
            "Days On Leave",
            "Days Absent",
            "Days Present",
        ],
        "data":[],
    }
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    cal = calendar.monthcalendar(year, month) 

    all_user = User.objects.all().order_by("id")
    for user in all_user:
        uname = "#"+str(user.id)+" "+user.name
        dept = user.department.name
        on_time_days = 0
        days_on_leave = 0
        days_absent = 0
        days_present = 0


        for week in cal:
            for day in week:
                if day == 0:
                    continue
                print(day)
                date = datetime.datetime(year, month, day)
                print(date)
                att = Attendance.objects.filter(time_stamp__date = date, user=user).order_by("-id")
                if len(att) == 2:
                    time_in = att[1].time_stamp.time()
                    time_out = att[0].time_stamp.time()

                    if time_in < user.shift.time_in:
                        days_present += 1
                        on_time_days += 1
                    else:
                        days_present +=1

                elif len(att) == 1:
                    if att[0].status=="absent":
                        days_on_leave += 1
                
                elif len(att) == 0:
                    days_absent += 1

        temp = [
            uname,
            dept,
            on_time_days,
            days_on_leave,
            days_absent,
            days_present,
        ]

        res["data"].append(temp)
    return res

def get_dept_daily(dept_id):
    res = {
        "title": "An organisational report on daily basis",
        "heading":[
            "Date",
            "User",
            "Dept",
            "Status",
            "Time In",
            "Time Out", 
            "Shift",
        ],
        "data" : [],
    }
    dept = Department.objects.get(id=dept_id)
    all_users = User.objects.filter(department=dept).order_by("id")
    

    for user in all_users:
        temp = get_user_daily(user)
        u_data = [
            temp["data"][0][1],
            temp["data"][0][0],
            user.department.name,
            temp["data"][0][2],
            temp["data"][0][3],
            temp["data"][0][4],
            temp["data"][0][5]+ " - "+temp["data"][0][6],            
        ]
        res["data"].append(u_data)
    return res

def get_dept_monthly(dept_id):
    res = {
        "title": "An organisational report for a month",
        "heading": [
            "User",
            "Dept",
            "On Time Days",
            "Days On Leave",
            "Days Absent",
            "Days Present",
        ],
        "data":[],
    }
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    cal = calendar.monthcalendar(year, month) 

    dept = Department.objects.get(id=dept_id)
    all_user = User.objects.filter(department=dept).order_by("id")
    for user in all_user:
        uname = "#"+str(user.id)+" "+user.name
        dept = user.department.name
        on_time_days = 0
        days_on_leave = 0
        days_absent = 0
        days_present = 0


        for week in cal:
            for day in week:
                if day == 0:
                    continue
                print(day)
                date = datetime.datetime(year, month, day)
                print(date)
                att = Attendance.objects.filter(time_stamp__date = date, user=user).order_by("-id")
                if len(att) == 2:
                    time_in = att[1].time_stamp.time()
                    time_out = att[0].time_stamp.time()

                    if time_in < user.shift.time_in:
                        days_present += 1
                        on_time_days += 1
                    else:
                        days_present +=1

                elif len(att) == 1:
                    if att[0].status=="absent":
                        days_on_leave += 1
                
                elif len(att) == 0:
                    days_absent += 1

        temp = [
            uname,
            dept,
            on_time_days,
            days_on_leave,
            days_absent,
            days_present,
        ]

        res["data"].append(temp)
    return res

@csrf_exempt
def mark_face_registered(request):
    res = {
        "error" : "",
        "content" : [],
        "success" : False,
    }
    if request.method == "POST":
        id = request.POST["id"]
        user = User.objects.filter(id=id)
        if len(user) != 0:
            user = user[0] 
            if user.is_registered:
                res["error"] = f"#{user.id} {user.name} is already registered"
            else:
                user.is_registered = True
                user.save()
                res["success"]= True

        else:
            res["error"] = f"No User exist with ID {id}"

    else:
        res["error"] = "Not a post request"

    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def mark_face_unregistered(request):
    res = {
        "success": False,
        "error": "",
        "content": "",
    }

    if request.method == "POST":
        id = request.POST["id"]
        user = User.objects.filter(id=id)
        if len(user) == 0:
            res["error"]= f"#{id} not a valid ID"
        else:
            user = user[0]
            if not user.is_registered:
                res["error"]= f"User #{id} {user.name} is already Unregistred"
            else:
                user.is_registered = False
                user.save()
                res["success"] = True

    else:
        res["error"] = "Not a POST request"

    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")



def default(o):
    if isinstance(o, (datetime.date, datetime.datetime, datetime.time)):
        return o.isoformat()

@csrf_exempt
def checkImageInput(request):
    res = {
        "success": False,
        "error": "",
        "content": "",
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print("the request is ajax")
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            # img = request.POST["img"]
            # print(data["imageData"])
            img = url_to_image(data["imageData"].split(",")[1]);
            name = data["name"]
            print("the name is "+name)
            # cv2.imshow("testimg",img);
            
            output_path = f'''C:\\Users\\gurpr\\Documents\\_StudyMaterial\\code\\afraas\\afraas_server_2\\reports\\face_data\\{name}.jpg'''
            # print(output_path)
            # Save the image using cv2.imwrite()

            label = test(
                image=img,
                model_dir=r'C:\Users\gurpr\Documents\_StudyMaterial\code\afraas\afraas_server_2\reports\resources\anti_spoof_models',
                device_id=0
            )
            if(label == 1):
                cv2.imwrite(output_path, img)
                res["success"] = True
                print("valid image")
            else:
                print("INvalid image")
                res["success"] = False


            
    else:
        res["error"] = "Not a POST Request";

    json_data = res
    json_data = json.dumps(json_data)
    return HttpResponse(json_data, content_type="application/json")

def url_to_image(data):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
	# resp = urlopen(url)
	# image = np.asarray(bytearray(url), dtype="uint8")

    binary_data = base64.b64decode(data)

    # Convert the binary data to a NumPy array
    image_array = np.frombuffer(binary_data, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
	# return the image
    return image
    