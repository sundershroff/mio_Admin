from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from rest_framework.response import Response
from django.contrib import messages
from collections import Counter




def dashboard(request):
    return render(request,"")

def shop(request):
    return render(request,"index.html")

def food(request):
    return render(request,"food_index.html")

def fresh_cuts(request):
    return render(request,"fresh_cuts_index.html")

def doriginal(request):
    return render(request,"doriginal_index.html")

def daily_mio(request):
    return render(request,"daily_mio_index.html")

def jewellery(request):
    return render(request,"jwellery_index.html")

def pharmacy(request):
    return render(request,"pharmacy_index.html")

