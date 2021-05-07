from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt 

def index(request):
    return render (request, "index.html")

def add(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'],password=hash_pwd)
        request.session['userid'] = user.id
        return redirect('/success')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['pwd'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect ('/success')
    else:
        pass
    return redirect('/')

def success(request):
    if request.method == "GET":
        context={
            'user':User.objects.get(id=request.session['userid'])
        }
        return render (request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')