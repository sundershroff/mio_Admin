from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from rest_framework.response import Response
from django.contrib import messages
from collections import Counter

jsondec = json.decoder.JSONDecoder()
def usersignup(request):
    error = ""
    if request.method == "POST":
        print(request.POST)
        if request.POST['password'] == request.POST['confirm_password']:
                response = requests.post("http://127.0.0.1:3000/end_user_signup/",data=request.POST)
                print(response.status_code)
                print(response.text)
                uidd = (response.text[1:-1]) 
                print(uidd)
                if response.status_code == 200:
                   return redirect(f"/enduser/end_user_otp/{uidd}")
                elif response.status_code == 302:
                    error = "User Already Exist"
        else:
            print("password doesn't match")
    context = {'error':error}
    return render(request,"enduser_signup.html",context)

def usersignin(request):

    error = ""
    if request.method == "POST":
        print(request.POST)
        response = requests.post("http://127.0.0.1:3000/end_user_signin/",data=request.POST)
        print(response.status_code)
        print(type(jsondec.decode(response.text)))
        print(jsondec.decode(response.text))
        uid = jsondec.decode(response.text)
        if response.status_code == 200:
            response = redirect(f"/enduser/dashboard/{uid}")
        else:
          error = "YOUR EMAILID OR PASSWORD IS INCORRECT"
    context = {'error':error}
    return render(request,"enduser_signin.html",context)

def otp(request,id):
    context = {'invalid':"invalid"}
    new=[]
    if request.method == "POST":
        new.append(request.POST["otp1"])
        new.append(request.POST["otp2"])
        new.append(request.POST["otp3"])
        new.append(request.POST["otp4"])
        data = {
            'user_otp':int(''.join(new).strip())
           
        }
        print(data)
        response = requests.post(f"http://127.0.0.1:3000/end_user_otp/{id}", data=data)

       
        print(response)
        print(response.status_code)
        print(data['user_otp'])
        print(response.text)
        uidd = (response.text[1:-1])
        
        if response.status_code == 200:

            return redirect(f"/enduser/profile_picture/{uidd}")
        else:
            invalid = "Invalid OTP"
            context = {'invalid':invalid}
    return render(request,"enduser_otpcheck.html",context)

def profile_picture(request,id):
    if request.method == "POST":
        print(request.FILES)
        response = requests.post(f"http://127.0.0.1:3000/end_profile_picture/{id}",   files=request.FILES)
        print(response)
        print(response.status_code)
        print(response.text)
        uidd = (response.text[1:-1])
        if response.status_code == 200:
        
            return redirect(f"/enduser/dashboard/{uidd}")
        else:
            return HttpResponse("INVALId")
    return render(request,"enduser_profilepic.html")



def dashboard(request,id):

    return render(request,"index.html")

def shop(request,id):
    mydata = requests.get("http://127.0.0.1:3000/shop_get_adminelectronics").json()[0]
    print(mydata)

    return render(request,"index.html")

def food(request):
    return render(request,"food_index.html")

def fresh_cuts(request):
    return render(request,"fresh_cuts_index.html")

def doriginal(request):
    return render(request,"doriginal_index.html")

def daily_mio(request):
    return render(request,"daily_mio_index.html")

def jewellery(request,id):
    return render(request,"jwellery_index.html")

def pharmacy(request):
    return render(request,"pharmacy_index.html")

