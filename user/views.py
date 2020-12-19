from django.http import HttpResponse
from django.shortcuts import  render
from .models import User
from django.contrib.auth.hashers import make_password

def index(request):
    return HttpResponse("Hello, world.")

def login(request):
    # return HttpResponse('hi')
    return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        try:
            name=request.POST["name"]
            password=make_password(request.POST["password"])
            mail=request.POST["email"]
            u=User(name=name,password=password,mail=mail)
            u.save()
            return render(request,'signup.html',{"success":True})
        except:
           return render(request,'signup.html',{"error":True})
    return render(request,'signup.html')

