from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from user.models import *


# Create your views here.
@login_required
def dashboard(request):
    context = {
        "title": "Admin | AFRAAS"
    }
    user = request.user
    if user.is_superuser:
        context["name"] = user.name
        return render(request, 'myadmin/dashboard.html',context)
    else:
        # Redirect to login page
        return HttpResponse("login first")
        return redirect('login')

@login_required
def users(request):
    return HttpResponse("all users")

@login_required
def shifts(request):
    context = {
        "title": "Shifts | AFRAAS"
    }
    user = request.user
    if user.is_superuser:
        context["name"] = user.name
        return render(request, 'myadmin/shifts.html',context)
    else:
        # Redirect to login page
        return HttpResponse("login first")
        return redirect('login')

@login_required
def departments(request):
    context = {
        "title": "Departments | AFRAAS"
    }
    curr_user = request.user
    if curr_user.is_superuser:
        context["name"] = curr_user.name

        if request.method == "POST":
            dept_name = request.POST["department_name"]
            dept = Department(name=dept_name)
            dept.save()

        all_dept = Department.objects.all()
        all_dept = list(all_dept)
        context["depts"] = []

        for dept in all_dept:
            obj = {
                'id': dept.id,
                'name' : dept.name
            }
            context["depts"].append(obj)


        return render(request, 'myadmin/departments.html',context)


    else:
        # Redirect to login page
        # return HttpResponse("login first")
        return redirect('staff:dashboard')

@login_required
def attendance(request):
    return HttpResponse("attendances table")