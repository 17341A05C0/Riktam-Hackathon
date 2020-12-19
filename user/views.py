from django.http import HttpResponse
from django.shortcuts import  render


def index(request):
    return HttpResponse("Hello, world.")

def login(request):
    # return HttpResponse('hi')
    return render(request,'login.html')

def signup(request):
    return HttpResponse('signup')