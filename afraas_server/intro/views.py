from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import  login
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect

from user.my_backend import EmailBackend


def landingPage(request):
    context={
        "title": "Welcome | AFRAAS"
    }
    
    return render(request, "intro/landing_page.html", context)

def _login(request):
    if request.method == 'POST':
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
            if user.is_superuser:
                next = reverse('myadmin:dashboard')
            
            elif user.is_staff:
                next = reverse('staff:dashboard')
            else:
                next = reverse('user:dashboard')
            
            return JsonResponse({'success': True, 'next': next})
        else:
            print("invalid")
            return JsonResponse({'success': False, 'error': 'Invalid credentials'})

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