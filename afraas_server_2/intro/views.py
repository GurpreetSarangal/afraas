from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import  login, logout
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect
import json
from user.my_backend import EmailBackend


def landingPage(request):
    context={
        "title": "Welcome | AFRAAS"
    }
    curr_user = request.user
    print(curr_user)

            
    if curr_user.is_staff:
        return redirect( reverse('staff:dashboard'))

    elif curr_user.is_authenticated:
        return redirect( reverse('user:dashboard'))
    
    return render(request, "intro/landing_page.html", context)

def _login(request):



    if request.method == "POST":
        res = {
                "content" : "",
                "error" : "",
                "success": False,

        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    
            email = request.POST['email']
            # print(email)
            password = request.POST['password']
            # print(password)
            eb = EmailBackend()
            user = eb.authenticate(request, email=email, password=password)
            # print(user)
        
            if user is not None:
                login(request, user)
                # print("valid")
                # print(user)
                # if user.is_superuser:
                #     next = "django-admin/"
                
                if user.is_staff:
                    next = reverse('staff:dashboard')
                else:
                    next = reverse('user:dashboard')
                
                res = {'success': True, 'next': next}
                json_data = json.dumps(res)
                return HttpResponse(json_data, content_type="application/json")
                return JsonResponse({'success': True, 'next': next})
            else:
                print("invalid")
                res = {'success': False, }
                json_data = json.dumps(res)
                return HttpResponse(json_data, content_type="application/json")

                return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        else:
            return HttpResponse("not an ajax request")

    elif request.method == "GET":
        return redirect("home")

    else:

        return HttpResponse("not a post request")


def _logout(request):
    if request.user:
        logout(request)
    return redirect("home")

def help(request):
    return HttpResponse("this is help page")

def developer_support(request):
    return HttpResponse("this is developer support page")

def credits(request):
    return HttpResponse("this is credits page")

def contact_us(request):
    return HttpResponse("this is contact us page")

def report_issue(request):
    return HttpResponse("this is report issue page")

def about_us(request):
    return HttpResponse("this is about us page")