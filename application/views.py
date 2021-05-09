from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import *
import bcrypt 

def index(request):
    return render (request, "index.html")

def add(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash_pwd = bcrypt.hashpw(request.POST['pwd'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], email=request.POST['email'],password=hash_pwd, birthday=request.POST['bday'])
            request.session['userid'] = user.id
            return redirect('/success')

def login(request):
    if request.method=="POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.filter(email=request.POST['email'])
            logged_user = user[0]
            request.session['userid'] = logged_user.id
            return redirect ('/success')

def success(request):
    context={
        'user':User.objects.get(id=request.session['userid'])
    }
    return render (request, "success.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')