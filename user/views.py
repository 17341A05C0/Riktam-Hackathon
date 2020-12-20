from django.http import HttpResponse
from django.shortcuts import  render,redirect
from .models import User, Issue, Message, Vote
from django.contrib.auth.hashers import make_password, check_password
import json
import crypt
from .forms import IssueForm
# from django.contrib.gis.utils import GeoIP

def index(request):
    if request.method == "POST":
        try:
            form = IssueForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.cleaned_data.get("image_field")
                caption=request.POST['caption']
                id=request.session['Id']
                # g = GeoIP()
                # ip = request.META.get('REMOTE_ADDR', None)
                # if ip:
                #     city = g.city(ip)['city']
                # else:
                #     city='Hyderabad'
                i=Issue(user=User.objects.get(pk=id),caption=caption,location=city,image=img)
                i.save()
                return HttpResponse('success')
        except Exception as e:
            return HttpResponse(e)

    elif request.session.get('Id'):
        name=request.session['Name']
        user_id=request.session['Id']
        issues=Issue.objects.all()
        messages=Message.objects.all()
        votes=Vote.objects.all()
        votes_user=list(map(lambda x:(x.user_id.id,x.issue_id.id),votes))

        return render(request,'index.html',{"name":name,"issues":issues,"messages":messages,
                                            "votes":json.dumps(votes_user),"id":user_id,"form":IssueForm()})
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
        a=list(map(lambda x:(x.mail,x.password,x.name,x.id),a))
        for i in a:
            if i[0]==mail:
                if check_password(password,i[1]):
                    request.session['Name']=i[2]
                    request.session['Id']=i[3]
                    return redirect('user:index')
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


def addvote(request):
    issue_id=request.POST['issue_id']
    user_id=request.session['Id']
    check=Vote.objects.filter(user_id=user_id,issue_id=issue_id)
    # return HttpResponse(len(check))
    x = Issue.objects.filter(id=issue_id)[0]
    l=len(check)
    if len(check)==0:
        x.votes+=1
        x.save()
        v=Vote(user_id=User.objects.get(pk=user_id),issue_id=Issue.objects.get(pk=issue_id))
        v.save()
    else:
        x.votes-=1
        x.save()
        check.delete()
    return HttpResponse(l)

def addmessage(request):
    issue_id=request.POST['issue_id']
    user_id=request.session['Id']
    msg=request.POST['msg']
    try:
        m=Message(message=msg,user_id=User.objects.get(pk=user_id),issue_id=Issue.objects.get(pk=issue_id))
        m.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")