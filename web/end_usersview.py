from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import json
from rest_framework.response import Response
from django.contrib import messages
from collections import Counter

jsondec = json.decoder.JSONDecoder()
#shopping Without user
def shop(request):
    shopdata = requests.get("http://127.0.0.1:3000/all_shopproducts").json()
    context={
        
    'key':shopdata,
    
        }
        
    return render(request,"index.html",context)

def shop_products(request,category):
    product_data=requests.get(f"http://127.0.0.1:3000/category_based_shop/{category}/").json()
    # print(product_data.content)
    print(type(product_data))
       
    context={
            'products' : product_data,
             }

    return render(request,"shop-left-sidebar.html",context)

def single_shopproducts(request,id,product_id):
   
    single_product=requests.get(f"http://127.0.0.1:3000/get_single_shopproduct/{id}/{product_id}").json()[0]
   
    print((single_product))

    context={
        'single' : single_product,
    }

    return render(request,"single-product.html",context)

def food(request):
    food_data= requests.get("http://127.0.0.1:3000/all_foodproducts/").json()
    print(food_data)

    context={
        'food':food_data
    }

    return render(request,"food_index.html",context)

def food_products(request,category):
    food_data=requests.get(f"http://127.0.0.1:3000/category_based_food/{category}/").json()
    # print(product_data.content)
    print((food_data))
       
    context={
            'foods' : food_data,
             }

    return render(request,"food_shop-left-sidebar.html",context)

def single_food_products(request,id,product_id):
    food_data=requests.get(f"http://127.0.0.1:3000/single_foodproduct/{id}/{product_id}").json()[0]
    # print(product_data.content)
    print((food_data))
       
    context={
            'foods': food_data,
             }

    return render(request,"food_single-product.html",context)

def fresh_cuts(request):
    fresh_data= requests.get("http://127.0.0.1:3000/all_freshcutproducts/").json()
    print(fresh_data)

    context={
        'fresh':fresh_data
    }

    return render(request,"fresh_cuts_index.html",context)

def fresh_cut_products(request,category):
    fresh_data=requests.get(f"http://127.0.0.1:3000/category_based_fresh/{category}/").json()
    # print(product_data.content)
    print(type(fresh_data))
       
    context={
            'fresh_cuts' : fresh_data,
             }

    return render(request,"fresh_cuts-left-sidebar.html",context)

def fresh_cut_singel_products(request,id,product_id):
    fresh_data=requests.get(f"http://127.0.0.1:3000/single_freshproduct/{id}/{product_id}").json()[0]
    # print(product_data.content)
    print((fresh_data))
       
    context={
            'fresh_cuts': fresh_data,
             }

    return render(request,"fresh_cuts_single-product.html",context)


def doriginal(request):
    dorigin_data= requests.get("http://127.0.0.1:3000/all_d_originalproducts/").json()
    print(dorigin_data)

    context={
        'dorigin':dorigin_data
    }
    return render(request,"doriginal_index.html",context)

def d_original_single_products(request,id,product_id):
    dorigin_data=requests.get(f"http://127.0.0.1:3000/single_d_originalproduct/{id}/{product_id}").json()[0]

    context={
        'd_origin' : dorigin_data
    }
    return render(request,"doriginal_single_product.html",context)

def daily_mio(request):
    dmio_data= requests.get("http://127.0.0.1:3000/all_dmioproducts/").json()
    print(dmio_data)

    context={
        'dmio':dmio_data
    }
    return render(request,"daily_mio_index.html",context)

def daily_mio_products(request,category):
    dmio_data= requests.get(f"http://127.0.0.1:3000/category_based_dmio/{category}/").json()
    print(dmio_data)

    context={
        'dmios':dmio_data
    }
    return render(request,"daily_mio_shop-left-sidebar.html",context)

def daily_mio_single_products(request,id,product_id):
    dmio_data= requests.get(f"http://127.0.0.1:3000/get_single_dmio_product/{id}/{product_id}").json()[0]
    print(dmio_data)

    context={
        'dmios':dmio_data
    }
    return render(request,"daily_mio_single_product.html",context)

def jewellery(request):
    jewel_data= requests.get("http://127.0.0.1:3000/all_jewelproducts/").json()
    print(jewel_data)

    context={
        'jewels': jewel_data
    }
    return render(request,"jwellery_index.html",context)

def jewellery_products(request,category):
    jewel_data= requests.get(f"http://127.0.0.1:3000/category_based_jewel/{category}/").json()
    print(jewel_data)

    context={
        'jewels': jewel_data
    }
    return render(request,"jwellery_shop-left-sidebar.html",context)

def jewellery_single_products(request,id,product_id):
    jewel_data= requests.get(f"http://127.0.0.1:3000/single_jewelproduct/{id}/{product_id}").json()[0]
    print(jewel_data)

    context={
        'jewels': jewel_data
    }
    return render(request,"jwellery_single_product.html",context)

def pharmacy(request):
    pharm_data= requests.get("http://127.0.0.1:3000/all_pharmproducts/").json()
    print(pharm_data)

    context={
        'pharms':pharm_data
    }
    return render(request,"pharmacy_index.html",context)

def pharmac_products(request,category):
    pharm_data= requests.get(f"http://127.0.0.1:3000/category_based_pharm/{category}/").json()
    print(pharm_data)

    context={
        'pharms':pharm_data
    }
    return render(request,"pharmacy_shop-left-sidebar.html",context)

def pharmac_single_products(request,id,product_id):
    pharm_data= requests.get(f"http://127.0.0.1:3000/single_pharmproduct/{id}/{product_id}").json()[0]
    print(pharm_data)
    
    context={
        'pharms':pharm_data
    }
    return render(request,"pharmacy_single-product.html",context)

# shopping with EndUser

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
        uid = jsondec.decode(response.text)
        if response.status_code == 200:
            mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{uid}").json()[0]
            print(mydata.get("otp"))
            if mydata.get("otp") == None:
                return redirect(f"/enduser/end_user_otp/{uid}")
            else:
                return redirect(f"/enduser/dashboard/{uid}")
        else:
          error = "YOUR USERNAME OR PASSWORD IS INCORRECT"
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
        response = requests.post(f"http://127.0.0.1:3000/end_profile_picture/{id}",  files=request.FILES)
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
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    shopdata = requests.get("http://127.0.0.1:3000/all_shopproducts").json()

    context={
        
    'key':mydata,
    'shopdata':shopdata,
    
        }
    return render(request,"user_dashboard.html",context)

def shopproduct_category(request,id,category):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    product_data=requests.get(f"http://127.0.0.1:3000/category_based_shop/{category}/").json()
    # print(product_data.content)   
    context={

            'key': mydata,
            'products' : product_data,

             }

    return render(request,"user_product_category.html",context)

def user_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    single_product=requests.get(f"http://127.0.0.1:3000/get_single_shopproduct/{shop_id}/{product_id}").json()[0]
    print(single_product)

    context={
        
        'key':mydata,
        'single':single_product,
    
        }

    return render(request,"single_shopproduct.html",context)


def shopping_cart(request):

    return render(request,"shopping-cart.html")

def shopping_checkout(request):

    return render(request,"checkout.html")

def order(request):
    shopdata = requests.get("http://127.0.0.1:3000/all_shopproducts").json()
    context={
        
    'key':shopdata,
    
        }     
    return render(request,"order.html",context)

# End user Food
def user_foodpage(request,id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    food_data= requests.get("http://127.0.0.1:3000/all_foodproducts/").json()
    print(food_data)

    context={
        'key' : mydata,
        'food':food_data,
    }

    return render(request,"user_food_index.html",context)

def food_products_category(request,id,category):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    food_data=requests.get(f"http://127.0.0.1:3000/category_based_food/{category}/").json()
    # print(product_data.content)
    print((food_data))
       
    context={
            'key' : mydata,
            'foods' : food_data,
             }

    return render(request,"user_food_category.html",context)

def user_singlefood_products(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    food_data=requests.get(f"http://127.0.0.1:3000/single_foodproduct/{shop_id}/{product_id}").json()[0]
   # print(product_data.content)
    print((food_data))
       
    context={
             'key' : mydata,
             'foods': food_data,
             }

    return render(request,"user_singlefood.html",context)

def user_fresh_cuts(request,id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    fresh_data= requests.get("http://127.0.0.1:3000/all_freshcutproducts/").json()
    print(fresh_data)

    context={
         'key' : mydata,
        'fresh':fresh_data,
    }

    return render(request,"user_freshcuts_index.html",context)

def user_freshcut_products(request,id,category):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    fresh_data=requests.get(f"http://127.0.0.1:3000/category_based_fresh/{category}/").json()
    # print(product_data.content)
    print(type(fresh_data))
       
    context={
            'key' : mydata,
            'fresh_cuts' : fresh_data,
             }

    return render(request,"user_freshcut_sidebar.html",context)

def user_freshcut_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    fresh_data=requests.get(f"http://127.0.0.1:3000/single_freshproduct/{shop_id}/{product_id}").json()[0]
    # print(product_data.content)
    print((fresh_data))
       
    context={
              'key': mydata,
            'fresh_cuts': fresh_data,
             }

    return render(request,"user_freshcut_single.html",context)


def user_doriginal(request,id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    dorigin_data= requests.get("http://127.0.0.1:3000/all_d_originalproducts/").json()
    print(dorigin_data)


    context={
      'key': mydata,
        'dorigin':dorigin_data
    }
    return render(request,"user_dorigin_index.html",context)

def user_doriginal_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    dorigin_data=requests.get(f"http://127.0.0.1:3000/single_d_originalproduct/{shop_id}/{product_id}").json()[0]

    context={
      'key':mydata,
        'd_origin' : dorigin_data
    }
    return render(request,"user_dorigin_single.html",context)

def user_daily_mio(request,id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    dmio_data= requests.get("http://127.0.0.1:3000/all_dmioproducts/").json()
    print(dmio_data)

    context={
      'key': mydata,
        'dmio':dmio_data
    }
    return render(request,"user_dmio.html",context)

def user_dmio_products(request,id,category):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    dmio_data= requests.get(f"http://127.0.0.1:3000/category_based_dmio/{category}/").json()
    print(dmio_data)

    context={
         'key':mydata,
        'dmios':dmio_data
    }
    return render(request,"user_dmio_category.html",context)

def user_dailymio_single_products(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    dmio_data= requests.get(f"http://127.0.0.1:3000/get_single_dmio_product/{shop_id}/{product_id}").json()[0]
    print(dmio_data)

    context={
          'key':mydata,
        'dmios':dmio_data
    }
    return render(request,"user_dmio_singlepage.html",context)

def user_jewellery(request,id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    jewel_data= requests.get("http://127.0.0.1:3000/all_jewelproducts/").json()
    print(jewel_data)

    context={
         'key':mydata,
        'jewels': jewel_data
    }
    return render(request,"user_jewels_index.html",context)

def user_jewellery_products(request,id,category):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    jewel_data= requests.get(f"http://127.0.0.1:3000/category_based_jewel/{category}/").json()
    print(jewel_data)

    context={
      'key': mydata,
        'jewels': jewel_data
    }
    return render(request,"user_jewel_shop.html",context)

def user_jewel_single_product(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    jewel_data= requests.get(f"http://127.0.0.1:3000/single_jewelproduct/{shop_id}/{product_id}").json()[0]
    print(jewel_data)

    context={
         'key':mydata,
        'jewels': jewel_data
    }
    return render(request,"user_jewels_singlepage.html",context)

def user_pharmacy(request,id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    pharm_data= requests.get("http://127.0.0.1:3000/all_pharmproducts/").json()
    print(pharm_data)

    context={
       'key': mydata,
        'pharms':pharm_data
    }
    return render(request,"user_pharmacy_index.html",context)

def user_pharm_products(request,id,category):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    pharm_data= requests.get(f"http://127.0.0.1:3000/category_based_pharm/{category}/").json()
    print(pharm_data)

    context={
       'key': mydata,
        'pharms':pharm_data
    }
    return render(request,"user_pharmacy_products.html",context)

def user_pharmac_singleproduct(request,id,shop_id,product_id):
    mydata = requests.get(f"http://127.0.0.1:3000/single_users_data/{id}").json()[0]
    pharm_data= requests.get(f"http://127.0.0.1:3000/single_pharmproduct/{shop_id}/{product_id}").json()[0]
    print(pharm_data)
    
    context={
       'key': mydata,
        'pharms':pharm_data
    }
    return render(request,"user_pharm_single.html",context)


