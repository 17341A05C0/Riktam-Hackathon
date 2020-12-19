from django.http import HttpResponse
from django.shortcuts import  render,redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password
import json
import crypt

def index(request):
    if request.session.get('Name'):
        name=request.session['Name']
        return render(request,'index.html',{"name":name})
    return redirect('user:login')

def login(request):

    a=User.objects.all()
    # for i in a[1:]:
    #     return HttpResponse(i)
    a=list(map(lambda x:(x.mail),a))
    # return HttpResponse(a)
    a=json.dumps(a)

    if request.method=="POST":
        mails=a
        mail=request.POST['email']
        password=request.POST['password']
        a=User.objects.all()
        a=list(map(lambda x:(x.mail,x.password,x.name),a))
        for i in a:
            if i[0]==mail:
                if check_password(password,i[1]):
                    request.session['Name']=i[2]
                    return HttpResponse("True")
        return render(request,'login.html',{"error":"Incorrect Details","mail":mail,"list":mails})

    return render(request,'login.html',{"list":a})

def signup(request):
    if request.method=="POST":
        try:
            name=request.POST["name"].lower()
            password=make_password(request.POST["password"])
            mail=request.POST["email"]
            u=User(name=name,password=password,mail=mail)
            u.save()
            return render(request,'signup.html',{"success":True})
        except:
           return render(request,'signup.html',{"error":True})
    a=User.objects.all()
    # for i in a[1:]:
    #     return HttpResponse(i)
    a=list(map(lambda x:x.mail,a))
    # return HttpResponse(a)
    a=json.dumps(a)
    return render(request,'signup.html',{"list":a})


