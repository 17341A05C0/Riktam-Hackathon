from django.http import HttpResponse
from django.shortcuts import  render,redirect
from .models import User, Issue, Message, Vote
from django.contrib.auth.hashers import make_password, check_password
import json
import crypt
from .forms import IssueForm
# from django.contrib.gis.utils import GeoIP

# import module
from geopy.geocoders import Nominatim

Choices = (
    (1, 'Submitted to the newspaper'),
    (2, 'resolved'),
    (3, 'no action taken'),
    (4, 'open')
)

def getLocation(Latitude,Longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Latitude & Longitude input
    # Latitude = "16.945529999999998"
    # Longitude = "82.2381173"

    location = geolocator.reverse(Latitude + "," + Longitude)

    address = location.raw['address']

    city = address.get('city', 'Hyderabad')
    state = address.get('state', 'Telangana')
    return city+", "+state

def getRecent():
    issues=Issue.objects.order_by('time')[::-1]
    messages=Message.objects.order_by('time')[::-1]

    l=[]
    for i in issues:
        l+=[(i.user.name.title(),"<b> "+i.caption+" </b>"," Posted a new Issue named ",i.time)]
    for i in messages:
        l+=[(i.user_id.name.title(),"<b> "+i.message+" </b>", " Messaged on "+i.issue_id.user.name.title()+"'s Issue as ",i.time)]
    l.sort(key=lambda x:x[-1],reverse=True)
    l=list(map(lambda x:x[:-1],l))
    l=l[:100]
    l=json.dumps(l)
    return l

def index(request):
    if request.method == "POST":
        try:
            form = IssueForm(request.POST, request.FILES)
            if form.is_valid():
                img = form.cleaned_data.get("image_field")
                caption=request.POST['caption']
                id=request.session['Id']
                lat=request.POST['lat']
                long=request.POST['long']
                # return HttpResponse(lat+" "+long)
                city=getLocation(lat,long)

                i=Issue(user=User.objects.get(pk=id),caption=caption,location=city,image=img)
                i.save()
                return HttpResponse('success')
        except Exception as e:
            return HttpResponse(e)

    elif request.session.get('Id'):
        name=request.session['Name']
        user_id=request.session['Id']
        issues=Issue.objects.order_by('time')[::-1]
        messages=Message.objects.all()[::-1]
        votes=Vote.objects.all()

        recent=getRecent()

        votes_user=list(map(lambda x:(x.user_id.id,x.issue_id.id),votes))


        return render(request,'index.html',{"name":name,"issues":issues,"messages":messages,
                                        "recent":recent,"votes":json.dumps(votes_user),"id":user_id,"form":IssueForm()})
    return redirect('user:login')

def logout(request):
    if request.session.get('Id'):
        del request.session['Id']
        del request.session['Name']
        try:
            del request.session['admin']
        except:
            pass
        return redirect('user:login')

def login(request):

    if request.session.get('Id'):
        return redirect('user:index')
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
        a=list(map(lambda x:(x.mail,x.password,x.name,x.id,x.is_admin),a))
        for i in a:
            if i[0]==mail:
                if check_password(password,i[1]):
                    request.session['Name']=i[2]
                    request.session['Id']=i[3]
                    if i[4]:
                        request.session['admin']=True

                        return redirect('user:admin')
                    return redirect('user:index')
        return render(request,'login.html',{"error":"Incorrect Details","mail":mail,"list":mails})

    return render(request,'login.html',{"list":a})

def signup(request):

    if request.session.get('Id'):
        return redirect('user:index')

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


def profile(request):
    if request.session.get('Id'):
        name=request.session['Name']
        user_id=request.session['Id']
        issues=Issue.objects.filter(user=User.objects.get(pk=user_id))
        messages=Message.objects.all()
        votes=Vote.objects.all()
        votes_user=list(map(lambda x:(x.user_id.id,x.issue_id.id),votes))

        recent=getRecent()

        return render(request,'profile.html',{"name":name,"issues":issues,"messages":messages,
                                           "recent":recent,"votes":json.dumps(votes_user),"id":user_id,"form":IssueForm()})
    return redirect('user:login')

def admin(request):
    if request.session.get('admin'):

        name=request.session['Name']
        user_id=request.session['Id']
        issues=Issue.objects.all()
        messages=Message.objects.all()

        choices=list(map(lambda x: Choices(int(x.status)-1),issues))

        return render(request,'admin.html',{"name":name,"issues":issues,"messages":messages,
                                            "id":user_id,"form":IssueForm()})

    if request.session.get('id'):
        return redirect('user:index')
    return redirect('user:login')


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

    if x.votes >= 100:
        x.status = 1
    else:
        x.status = 4
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

def editTitle(request):
    try:
        issue_id=request.POST['issue_id']
        # return HttpResponse(request.POST.items())
        caption=request.POST['caption']
        # return HttpResponse(caption+'hi')
        i=Issue.objects.get(pk=issue_id)
        i.caption=caption
        i.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse(e)

def deleteIssue(request):
    try:
        issue_id = request.POST['issue_id']
        i=Issue.objects.get(pk=issue_id)
        i.delete()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def deleteMessage(request):
    try:
        message_id = request.POST['message_id']
        m=Message.objects.get(pk=message_id)
        m.delete()
        return HttpResponse("True")
    except:
        return HttpResponse("False")
