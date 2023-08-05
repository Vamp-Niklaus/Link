from django.shortcuts import render, redirect,HttpResponse
from datetime import datetime
from slave.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import pre_save,post_save
import math

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        us=User.objects.get(username=request.user).id
        us=Users.objects.get(user_id=us).user_id
        context={}
        fl=link_list.objects.filter(u_id=us).first()
        if fl is None:
            context={
                "l":None,
                "cat":None
            }
        else:
            al=link_list.objects.filter(u_id=us).values_list('l_id',flat=True)
            obj=link_list.objects.filter(l_id__in =al)
            uc = obj.values_list('category', flat=True).distinct()
            context={
                "l":obj,
                "cat":list(uc)
            }
        return render(request,'index.html',context)
    return redirect('signin')

def save(request):
    if request.method == "POST":
        us=User.objects.get(username=request.user).id
        us=Users.objects.get(user_id=us).user_id
        link = request.POST['link']
        name = request.POST['name']
        remark = request.POST['remark']
        cat = request.POST['cat']
        if(len(cat)==0):
            cat="None"
        link_list(u_id=Users.objects.get(user_id=us),category=cat,remark=remark,link=link,name=name).save()
        return redirect('home')
    return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        gender = request.POST['gender']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        Users(id=User.objects.get(username=username).id,birthday=dob,gender=gender,user_id=User.objects.get(username=username).id).save()
        messages.success(request, "Your Account has been created succesfully!!")
        messages.success(request, "Logged In Sucessfully!!")
        user = authenticate(username=username, password=pass1)
        login(request, user)
        return redirect('home')
        
    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    return render(request, "signin.html")



def signout(request):
    logout(request)
    messages.success(request,"Logged out sucessfully!")
    return render(request, "signin.html")

