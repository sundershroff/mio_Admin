from django.shortcuts import render
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# Create your views here.
def index(request):
    return render(request,'admin_index.html')

def dashboard(request):
    return render(request,'admin_dashboard.html')

def product_details(request):
    return render(request,'admin_product_details.html')

def order_details(request):
    
    return render(request,'admin_orderlist.html')

def banner(request):
    return render(request,'admin_banner.html')

def customer_service(request):
    return render(request,'admin_customer_service.html')

def product_appaoval(request):
    db = client['business']
    collection = db['shopelectronics']
    
    shop_product = collection.find({})
    # for i in shop_product:
    #     print(i)
    print(shop_product)
    context = {
        'shopping':shop_product
    }   
    return render(request,'admin_product_appaoval.html',context)

def hub_details(request):
    return render(request,'admin_hub_details.html')

def hub_menu1(request):
    return render(request,'admin_hub_menu1.html')

def user_add(request):
    return render(request,'admin_usar_add.html')

def user_menu(request):
    return render(request,'admin_user_menu.html')









