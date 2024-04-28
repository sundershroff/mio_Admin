from django.shortcuts import render,redirect
from pymongo import MongoClient
from api.models import *
from mio_admin.models import *
import requests

client = MongoClient('localhost', 27017)

# Create your views here.
def index(request):
    return render(request,'admin_index.html')

def dashboard(request):
    return render(request,'admin_dashboard.html')

def product_details(request):
    shopping = shoppingmodel.objects.filter(category = "shopping")
    food = foodmodel.objects.filter(category = "food")
    fresh_cuts = freshcutsmodel.objects.filter(category = "fresh_cuts")
    daily_mio = dailymio_model.objects.filter(category = "daily_mio")
    pharmacy = pharmacy_model.objects.filter(category = "pharmacy")
    d_original = d_originalmodel.objects.filter(category = "d_original")
    jewellery = jewellerymodel.objects.filter(category = "jewellery")
    if request.method == "POST":    
        print(request.POST)
        if "region_select" in request.POST:
            if request.POST['region_select'] == "nagercoil":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "nagercoil",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "nagercoil",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "nagercoil",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "nagercoil",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "nagercoil",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "nagercoil",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "nagercoil",category = "jewellery")
            elif request.POST['region_select'] == "kanniyakumari":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "kanniyakumari",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "kanniyakumari",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "kanniyakumari",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "kanniyakumari",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "kanniyakumari",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "kanniyakumari",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "kanniyakumari",category = "jewellery")
        
            elif request.POST['region_select'] == "thuckalay":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "thuckalay",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "thuckalay",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "thuckalay",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "thuckalay",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "thuckalay",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "thuckalay",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "thuckalay",category = "jewellery")
            
            elif request.POST['region_select'] == "marthandam":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "marthandam",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "marthandam",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "marthandam",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "marthandam",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "marthandam",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "marthandam",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "marthandam",category = "jewellery")
            
            elif request.POST['region_select'] == "karungal":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "karungal",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "karungal",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "karungal",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "karungal",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "karungal",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "karungal",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "karungal",category = "jewellery")
            
            elif request.POST['region_select'] == "nithiravilai":
                #shopping
                shopping = shoppingmodel.objects.filter(region = "nithiravilai",category = "shopping")
                #foods
                food = foodmodel.objects.filter(region = "nithiravilai",category = "food")
                #fresh_cuts
                fresh_cuts = freshcutsmodel.objects.filter(region = "nithiravilai",category = "fresh_cuts")
                #daily_mio
                daily_mio = dailymio_model.objects.filter(region = "nithiravilai",category = "daily_mio")
                #pharmacy
                pharmacy = pharmacy_model.objects.filter(region = "nithiravilai",category = "pharmacy")
                #d_original
                d_original = d_originalmodel.objects.filter(region = "nithiravilai",category = "d_original")
                #jwellery
                jewellery = jewellerymodel.objects.filter(region = "nithiravilai",category = "jewellery")

    context = {
        "shopping":shopping,
        'food':food,
        'fresh_cuts':fresh_cuts,
        'daily_mio':daily_mio,
        'pharmacy':pharmacy,
        'd_original':d_original,
        'jewellery':jewellery,
    }
    return render(request,'admin_product_details.html',context)

def order_details(request):
    shopping = Product_Ordermodel.objects.filter(category_data = "shopping")
    food = Product_Ordermodel.objects.filter(category_data = "food")
    fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts")
    daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio")  
    pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy")  
    d_original = Product_Ordermodel.objects.filter(category_data = "d_original")
    jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery")
    if request.method == "POST":
        print(request.POST)
        if "region_select" in request.POST:
            if request.POST['region_select'] == "nagercoil":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",end_user__region = "nagercoil")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "nagercoil")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "nagercoil")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "nagercoil")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "nagercoil")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "nagercoil")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "nagercoil")
            elif request.POST['region_select'] == "kanniyakumari":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "kanniyakumari")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "kanniyakumari")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "kanniyakumari")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "kanniyakumari")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "kanniyakumari")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "kanniyakumari")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "kanniyakumari")
        
            elif request.POST['region_select'] == "thuckalay":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "thuckalay")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "thuckalay")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "thuckalay")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "thuckalay")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "thuckalay")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "thuckalay")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "thuckalay")
            
            elif request.POST['region_select'] == "marthandam":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "marthandam")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "marthandam")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "marthandam")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "marthandam")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "marthandam")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "marthandam")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "marthandam")
            
            elif request.POST['region_select'] == "karungal":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "karungal")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "karungal")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "karungal")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "karungal")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "karungal")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "karungal")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "karungal")
            
            elif request.POST['region_select'] == "nithiravilai":
                shopping = Product_Ordermodel.objects.filter(category_data = "shopping",region = "nithiravilai")
                food = Product_Ordermodel.objects.filter(category_data = "food",region = "nithiravilai")
                fresh_cuts = Product_Ordermodel.objects.filter(category_data = "fresh_cuts",region = "nithiravilai")
                daily_mio = Product_Ordermodel.objects.filter(category_data = "daily_mio",region = "nithiravilai")  
                pharmacy = Product_Ordermodel.objects.filter(category_data = "pharmacy",region = "nithiravilai")  
                d_original = Product_Ordermodel.objects.filter(category_data = "d_original",region = "nithiravilai")
                jwellery = Product_Ordermodel.objects.filter(category_data = "jewellery",region = "nithiravilai")
    context = {
        'shopping':shopping,
        'food':food,
        'fresh_cuts':fresh_cuts,
        'daily_mio':daily_mio,
        'pharmacy':pharmacy,
        'd_original':d_original,
        'jwellery':jwellery,
    }
    return render(request,'admin_orderlist.html',context)

def bannerr(request):
    shopping = banner.objects.get(id = 1)
    food = banner.objects.get(id = 2)
    fresh_cuts = banner.objects.get(id = 3)
    daily_mio = banner.objects.get(id = 4)
    pharmacy = banner.objects.get(id = 5)
    d_original = banner.objects.get(id = 6)
    jewellery = banner.objects.get(id = 7)
    context = {
        'shopping':shopping,
        'food':food,
        'fresh_cuts':fresh_cuts,
        'daily_mio':daily_mio,
        'pharmacy':pharmacy,
        'd_original':d_original,
        'jewellery':jewellery,
        
    }
    if request.method == "POST":
        print(request.FILES)
        if "banner" in request.POST:
            data = banner.objects.get(id = request.POST['banner'])
            if "banner1" in request.FILES:
                data.banner1 = request.FILES['banner1']
            if "banner2" in request.FILES:
                data.banner2 = request.FILES['banner2']
        elif "ad" in request.POST:
            data = banner.objects.get(id = request.POST['ad'])
            if "ad1" in request.FILES:
                data.ad1 = request.FILES['ad1']
            if "ad2" in request.FILES:
                data.ad2 = request.FILES['ad2']
        data.save()
        return redirect("/admin_banner/")
    return render(request,'admin_banner.html',context)

def customer_service(request):
    return render(request,'admin_customer_service.html')

def product_appaoval(request):
    #shopping
    shop_product = shop_productsmodel.objects.all()
    shop_product_length = shop_productsmodel.objects.filter(status = "False")
    #foods
    food_product = food_productsmodel.objects.all()
    food_product_length = food_productsmodel.objects.filter(status = "False")
    #fresh_cuts
    fresh_cuts = fresh_productsmodel.objects.all()
    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False")
    #daily_mio
    daily_mio = dmio_productsmodel.objects.all()
    daily_mio_length = dmio_productsmodel.objects.filter(status = "False")
    #pharmacy
    pharmacy = pharmacy_productsmodel.objects.all()
    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False")
    #d_original
    d_original = d_original_productsmodel.objects.all()
    d_original_length = d_original_productsmodel.objects.filter(status = "False")
    #jwellery
    jwellery = jewel_productsmodel.objects.all()
    jwellery_length = jewel_productsmodel.objects.filter(status = "False")
    if request.method == "POST":
        print(request.POST)
        if "region_select" in request.POST:
            if request.POST['region_select'] == "nagercoil":
                #shopping
                shop_product = shop_productsmodel.objects.filter(region = "nagercoil")
                shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #foods
                food_product = food_productsmodel.objects.filter(region = "nagercoil")
                food_product_length = food_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #fresh_cuts
                fresh_cuts = fresh_productsmodel.objects.filter(region = "nagercoil")
                fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #daily_mio
                daily_mio = dmio_productsmodel.objects.filter(region = "nagercoil")
                daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #pharmacy
                pharmacy = pharmacy_productsmodel.objects.filter(region = "nagercoil")
                pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #d_original
                d_original = d_original_productsmodel.objects.filter(region = "nagercoil")
                d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "nagercoil")
                #jwellery
                jwellery = jewel_productsmodel.objects.filter(region = "nagercoil")
                jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "nagercoil")
        
            elif request.POST['region_select'] == "kanniyakumari":
                #shopping
                shop_product = shop_productsmodel.objects.filter(region = "kanniyakumari")
                shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #foods
                food_product = food_productsmodel.objects.filter(region = "kanniyakumari")
                food_product_length = food_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #fresh_cuts
                fresh_cuts = fresh_productsmodel.objects.filter(region = "kanniyakumari")
                fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #daily_mio
                daily_mio = dmio_productsmodel.objects.filter(region = "kanniyakumari")
                daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #pharmacy
                pharmacy = pharmacy_productsmodel.objects.filter(region = "kanniyakumari")
                pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #d_original
                d_original = d_original_productsmodel.objects.filter(region = "kanniyakumari")
                d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
                #jwellery
                jwellery = jewel_productsmodel.objects.filter(region = "kanniyakumari")
                jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "kanniyakumari")
        
            elif request.POST['region_select'] == "thuckalay":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "thuckalay")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "thuckalay")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "thuckalay")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "thuckalay")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "thuckalay")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "thuckalay")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "thuckalay")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "thuckalay")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "thuckalay")
            
            elif request.POST['region_select'] == "marthandam":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "marthandam")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "marthandam")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "marthandam")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "marthandam")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "marthandam")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "marthandam")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "marthandam")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "marthandam")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "marthandam")
            
            elif request.POST['region_select'] == "karungal":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "karungal")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "karungal")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "karungal")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "karungal")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "karungal")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "karungal")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "karungal")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "karungal")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "karungal")
            
            elif request.POST['region_select'] == "nithiravilai":
                #shopping
                    shop_product = shop_productsmodel.objects.filter(region = "nithiravilai")
                    shop_product_length = shop_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #foods
                    food_product = food_productsmodel.objects.filter(region = "nithiravilai")
                    food_product_length = food_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #fresh_cuts
                    fresh_cuts = fresh_productsmodel.objects.filter(region = "nithiravilai")
                    fresh_cuts_length = fresh_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #daily_mio
                    daily_mio = dmio_productsmodel.objects.filter(region = "nithiravilai")
                    daily_mio_length = dmio_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #pharmacy
                    pharmacy = pharmacy_productsmodel.objects.filter(region = "nithiravilai")
                    pharmacy_length = pharmacy_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #d_original
                    d_original = d_original_productsmodel.objects.filter(region = "nithiravilai")
                    d_original_length = d_original_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
                    #jwellery
                    jwellery = jewel_productsmodel.objects.filter(region = "nithiravilai")
                    jwellery_length = jewel_productsmodel.objects.filter(status = "False" , region = "nithiravilai")
            
        else:
            productid = request.POST['product_id']
            status = request.POST['status']
            category = request.POST['category']
            if category == "shopping":
                if status == "True":
                    update = shop_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = shop_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "food":
                if status == "True":
                    update = food_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = food_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "fresh_cuts":
                if status == "True":
                    update = fresh_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = fresh_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "daily_mio":
                if status == "True":
                    update = dmio_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = dmio_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "pharmacy":
                if status == "True":
                    update = pharmacy_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = pharmacy_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "d_original":
                if status == "True":
                    update = d_original_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = d_original_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            elif category == "jewellery":
                if status == "True":
                    update = jewel_productsmodel.objects.get(product_id = productid)
                    update.status = status
                    update.save()
                elif status == "Reject":
                    update = jewel_productsmodel.objects.get(product_id = productid)
                    product = update.product
                    product['reason'] = request.POST['reason']
                    update.status = status
                    update.product = product
                    update.save()
            print("update successfully")
    context = {
        'shopping':shop_product,
        'shop_product_length':shop_product_length,
        "food_product":food_product,
        'food_product_length':food_product_length,
        'fresh_cuts':fresh_cuts,
        'fresh_cuts_length':fresh_cuts_length,
        'daily_mio':daily_mio,
        'daily_mio_length':daily_mio_length,
        'pharmacy':pharmacy,
        'pharmacy_length':pharmacy_length,
        'd_original':d_original,
        'd_original_length':d_original_length,
        'jwellery':jwellery,
        'jwellery_length':jwellery_length,
        
        
    }   

    return render(request,'admin_product_appaoval.html',context)

def edit_product(request,product_id,category):
    print(category)
    if "shopping" == category:
        product = shop_productsmodel.objects.get(product_id = product_id)
        for_custom_description = shop_productsmodel.objects.get(product_id = product_id)
    elif "food" == category:
        product = food_productsmodel.objects.get(product_id = product_id)
        for_custom_description = food_productsmodel.objects.get(product_id = product_id)
    elif "fresh_cuts" == category:
        product = fresh_productsmodel.objects.get(product_id = product_id)
        for_custom_description = fresh_productsmodel.objects.get(product_id = product_id)
    elif "daily_mio" == category:
        product = dmio_productsmodel.objects.get(product_id = product_id)
        for_custom_description = dmio_productsmodel.objects.get(product_id = product_id)
    elif "pharmacy" == category:
        product = pharmacy_productsmodel.objects.get(product_id = product_id)
        for_custom_description = pharmacy_productsmodel.objects.get(product_id = product_id)
    elif "d_original" == category:
        product = d_original_productsmodel.objects.get(product_id = product_id)
        for_custom_description = d_original_productsmodel.objects.get(product_id = product_id)
    elif "jewellery" == category:
        product = jewel_productsmodel.objects.get(product_id = product_id)
        for_custom_description = jewel_productsmodel.objects.get(product_id = product_id)

    custom_description = for_custom_description.product
    # custom_description.pop("name")
    # custom_description.pop("brand")
    # custom_description.pop("actual_price")
    # custom_description.pop("discount_price")
    # custom_description.pop("status")
    # custom_description.pop("category")
    # custom_description.pop("subcategory")
    # custom_description.pop("shop_id")
    # custom_description.pop("product_id")
    # custom_description.pop("primary_image")
    # custom_description.pop("other_images")
    # custom_description.pop("selling_price")
    # custom_description.pop("reason")
    # print(custom_description)
    context = {
        "shop_product":product,
        "custom_description":custom_description,
    }
    if request.method == "POST":
        print(request.POST)
        print(request.FILES)
        print(product.category)
    return render(request,'product_edit.html',context)

    

def hub_details(request):
    if request.method == "POST":
        print(request.POST)
        create = Hub_CustomUser.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = request.POST['password'],
            phonenumber = request.POST['phonenumber'],
            hub = request.POST['hub'],
            door_no = request.POST['door_no'],
            street = request.POST['street'],
            city = request.POST['city'],
            state = request.POST['state'],
            country = request.POST['country']
        )
        create.save()
        return redirect("/admin_hub_menu1/")
    return render(request,'admin_hub_details.html')

def hub_menu1(request):
    data = Hub_CustomUser.objects.all()
    context = {
        'data':data
    }
    if request.method == "POST":
        dele = Hub_CustomUser.objects.get(id  = request.POST['delete'])
        dele.delete()
        return redirect("/admin_hub_menu1/")
    return render(request,'admin_hub_menu1.html',context)

def hub_update(request,id):
    data = Hub_CustomUser.objects.get(id = id)
    context={
        'data':data
    }
    if request.method == "POST":
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.username = request.POST['username']
        data.password = request.POST['password']
        data.phonenumber = request.POST['phonenumber']
        data.hub = request.POST['hub']
        data.door_no = request.POST['door_no']
        data.street = request.POST['street']
        data.city = request.POST['city']
        data.state = request.POST['state']
        data.country = request.POST['country']
        data.save()
        return redirect("/admin_hub_menu1/")
    return render(request,"hub_user_update.html",context)



def user_add(request):
    if request.method == "POST":
        print(request.POST)
        create = admin_CustomUser.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            username = request.POST['username'],
            password = request.POST['password'],
            phonenumber = request.POST['phonenumber'],
            access_priveleges = request.POST.getlist('access_priveleges')
        )
        create.save()
        return redirect("/admin_user_menu/")
    return render(request,'admin_usar_add.html')

def user_menu(request):
    data = admin_CustomUser.objects.all()
    context = {
        'data':data
    }
    if request.method == "POST":
        dele = admin_CustomUser.objects.get(id  = request.POST['delete'])
        dele.delete()
        return redirect("/admin_user_menu/")
    return render(request,'admin_user_menu.html',context)


def user_update(request,id):
    data = admin_CustomUser.objects.get(id = id)
    context={
        'data':data
    }
    if request.method == "POST":
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.username = request.POST['username']
        data.password = request.POST['password']
        data.phonenumber = request.POST['phonenumber']
        data.access_priveleges = request.POST.getlist('access_priveleges')
        data.save()
        return redirect("/admin_user_menu/")
    return render(request,"admin_user_update.html",context)

def customer(request):
    data = End_Usermodel.objects.all()
    context = {
        'data':data
    }
    return render(request,'customer_menu.html',context)

def delivery_boy_add(request):
    error = ""
    if request.POST:
        print(request.POST)
        print(request.FILES)
        print(dict(request.POST))
        # product={}
        # for x in dict(request.POST):
        #     print(x)
        #     product[x] = dict(request.POST)[x][0]
        # print(product)
        Response = requests.post("http://127.0.0.1:3000/delivery_person_signup/",data = request.POST,files=request.FILES)
        print(Response)
        print(Response.status_code)
        if Response.status_code == 200:
            return redirect("/admin/delivery_boy_manage/")
        elif Response.status_code == 302:
            error = "Email Id Already Existed"
    context= {
            'error':error,
        }
    return render(request,'deliveryboy_add.html',context)

def delivery_boy_manage(request):
    data  = Delivery_model.objects.all()
    
    context = {
        'data':data,
    }
    if request.method == "POST":
        print(request.POST)
        update_data = Delivery_model.objects.get(uid = request.POST['uid'])
        update_data.approve_status = request.POST['status']
        update_data.save()
    return render(request,'deliverboy_menu.html',context)

def delivery_boy_single(request,id):
    data = Delivery_model.objects.get(uid = id)
    context={
        'data':data,
    }
    return render(request,'deliverboy_single.html',context)

def delivery_Commision(request):
    data = comission_Editing.objects.get(id = 1)
    context = {
        'data':data
    }
    if request.method == "POST":
        data.per_km = request.POST['per_km']
        data.incentive = request.POST['incentive']
        data.save()
        return redirect("/admin/delivery_Commision/")
    return render(request,'delivery_commision.html',context)

def business_Commision(request):
    data = business_commision.objects.get(id = 1)
    context = {
        'data':data
    }
    if request.method == "POST":
        data.commission = request.POST['commission']
        data.gst = request.POST['gst']
        data.save()
        return redirect("/admin/business_Commision/")

    return render(request,'business_commsion.html',context)


def shutdown(request):
    if request.method == "POST":
        print(request.POST)
        
        
    return render(request,'showdown.html')

def zonee(request):
    data = zone.objects.all()
    context = {
        'zone':data
    }
    if request.method == "POST":
        print(request.POST)
        if "create" in request.POST:
            create = zone.objects.create(
                zone = request.POST['zone'].lower()
            )
            create.save()
        elif "add_zone" in request.POST:
            
            add = zone.objects.get(zone = request.POST['zone'])
            try:
                pincodee=add.pincode
                pincodee.append(request.POST['pincode'])
            except:
                pincodee = []
                pincodee.append(request.POST['pincode'])
            
            print(pincodee)
            add.pincode = pincodee
            add.save()
        elif "delete_pincode" in request.POST:
            deletepincode = zone.objects.get(zone = request.POST['delete_pincode'])
            pincode = deletepincode.pincode
            pincode.remove(request.POST['pincode'])
            deletepincode.pincode = pincode
            deletepincode.save()
        elif "delete_zone" in request.POST:
            deletezone = zone.objects.get(zone = request.POST['delete_zone'])
            print(deletezone)
            deletezone.delete()
        return redirect("/admin/zone/")
    return render(request,'zone.html',context)







