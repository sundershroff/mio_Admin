from django.shortcuts import render,get_object_or_404
from api.models import Businessmodel,shoppingmodel,jewellerymodel,foodmodel,freshcutsmodel,pharmacy_model,d_originalmodel,dailymio_model
from api import business_serializers
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import business_extension
from rest_framework.decorators import api_view
from api import models
import json
import datetime
from pymongo import MongoClient
from bson.json_util import dumps,loads
from django.db.models import Sum
from django.utils import timezone
import datetime
from django.db.models import Q


client = MongoClient('localhost', 27017)

all_image_url = "http://127.0.0.1:3000/"
x = datetime.datetime.now()

@api_view(['POST'])
def business_signup(request):
    try:
        try:
            if business_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'uid': business_extension.id_generate(),
                    'otp': business_extension.otp_generate(),
                    'full_name':request.data["full_name"],
                    'email': request.data["email"],
                    'phone_number': request.data["phone_number"],
                    'password': request.data["password"],
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = business_serializers.SignupSerializer(data=datas)
                print(dataserializer)
                print(datas['uid'])
                if dataserializer.is_valid():
                    print("valid")
                    dataserializer.save()
                    print("Valid Data")
                    business_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def business_otp(request, id):
    try:
        try:
            if business_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userData = Businessmodel.objects.get(uid=id)
                    print(userData)
                    serializer_validate = business_serializers.OTPSerializer(
                        instance=userData, data=request.POST, partial=True)
                    if serializer_validate.is_valid():
                        serializer_validate.save()
                        print("Valid OTP")
                        return Response(id, status=status.HTTP_200_OK)
                    else:
                        return Response({"Cannot Verify OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except:
                    return Response({"serializer Issue"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"Wrong OTP"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def business_signin(request):
    try:
       
        try:
            if business_extension.validate_email(request.data['email']):
                if business_extension.verify_user(request.data['email'], request.data['password']):
                    if business_extension.verify_user_otp(request.data['email']):
                        if business_extension.get_user_id(request.data['email']):
                            return Response(business_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
                        else:
                            return Response({"Didn't Completed OTP Verification"}, status=status.HTTP_401_UNAUTHORIZED)

                else:
                    return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"User Dosn't Exits"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def resend_otp(request,id):

    try:
        try:
            new_otp = business_extension.otp_generate()
            user = Businessmodel.objects.get(uid=id)
            email = user.email 
            print(f"Email: {email}")
            business_extension.send_mail(email, new_otp)
            user.otp = new_otp
            user.save()
            return Response({"New OTP": new_otp, "Email": email}, status=status.HTTP_200_OK)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def my_accounts_data(request,id):
    if request.method == 'GET':
       allDataa = Businessmodel.objects.filter(uid=id)
       alldataserializer = business_serializers.BusinessSerializer(allDataa,many=True)
    return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def forget_password(request):

    try:
        try:
            print(request.POST)
            if business_extension.validate_email(request.data['email']):
                Data = Businessmodel.objects.get(email=request.data['email'])

                data1={
                    'email':request.data['email'],
                    'password':request.data['password']
                }
                print(data1)
                basicdetailsserializer = business_serializers.forget_password_serializer(instance=Data, data=data1,partial=True)
                if basicdetailsserializer.is_valid():
                    basicdetailsserializer.save()
                    print("Valid Data")
                    return Response("password updated", status=status.HTTP_200_OK)                        
                else:
                    return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"User Dosn't Exits"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def business_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = Businessmodel.objects.get(uid=id)
        
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
     
        print(id)
        path = fs.save(f"api/business/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path
           
        }

        print(data)
        basicdetailsserializer = business_serializers.profile_picture_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# shop_dashboard
    
@api_view(['GET'])
def shop_total_revenue(request, id):
    if request.method == 'GET':
        total_revenue = models.shop_ordermodel.objects.filter(shop_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        shop = models.shoppingmodel.objects.get(shop_id=id)
        shop.total_revenue = total_revenue
        shop.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def shop_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.shop_ordermodel.objects.filter(shop_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        shop = models.shoppingmodel.objects.get(shop_id=id)
        shop.monthly_revenue = monthly_revenue
        shop.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def shop_orderstatus(request,id):
    if request.method == 'GET':

        shop = models.shop_ordermodel.objects.filter(shop_id=id).first()
        if not shop:
            return Response(data={'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.shop_ordermodel.objects.filter(shop_id=id, status='delivered').count()
        cancelled_count = models.shop_ordermodel.objects.filter(shop_id=id, status='cancelled').count()
        on_process_count = models.shop_ordermodel.objects.filter(shop_id=id, status='on_process').count()
        # delivered_count = delivered_count if delivered_count else 0
        # cancelled_count = cancelled_count if cancelled_count else 0
        # on_process_count = on_process_count if on_process_count else 0
        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def product_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.shop_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def product_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.shop_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def product_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.shop_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def shop_all_products(request,id):
    if request.method== "GET":
        elec_data = models.shop_electronicsmodel.objects.filter(shop_id=id)
        mob_data = models.shop_mobilemodel.objects.filter(shop_id=id)
        fur_data = models.shop_furnituremodel.objects.filter(shop_id=id)        
        auto_data = models.shop_autoaccessoriesmodel.objects.filter(shop_id=id)
        kitc_data = models.shop_kitchenmodel.objects.filter(shop_id=id)
        fas_data = models.shop_fashionmodel.objects.filter(shop_id=id)
        app_data = models.shop_appliancesmodel.objects.filter(shop_id=id)
        groc_data = models.shop_groceriesmodel.objects.filter(shop_id=id)
        pet_data = models.shop_petsuppliesmodel.objects.filter(shop_id=id)
        toy_data = models.shop_toysmodel.objects.filter(shop_id=id)        
        sport_data = models.shop_sportsmodel.objects.filter(shop_id=id)
        heal_data = models.shop_healthcaremodel.objects.filter(shop_id=id)
        book_data = models.shop_booksmodel.objects.filter(shop_id=id)
        pers_data = models.shop_personalcaremodel.objects.filter(shop_id=id)
        all_data = [
            elec_data, mob_data, fur_data, auto_data, kitc_data,
            fas_data, app_data, groc_data, pet_data, toy_data,
            sport_data, heal_data, book_data, pers_data
        ]
        # Calculate the total count
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)
    

# shopping 
@api_view(['POST'])
def shopping(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/shopping/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/shopping/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/shopping/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/shopping/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/shopping/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    shopping_id=business_extension.shop_id_generate()
    while True:
        if id == shopping_id:
            shopping_id=business_extension.shop_id_generate()
        else:
            break

    data = {
        'Business_id': id,
        'shop_id': shopping_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
        }
      
    print(data)
    basicdetailsserializer = business_serializers.shopping_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def shopping_alldata(request):
    if request.method == "GET":
        data = shoppingmodel.objects.all()
        serializer = business_serializers.shopping_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_shopping_data(request,id):
    if request.method == "GET":
        data = shoppingmodel.objects.get(shop_id=id)
        serializer = business_serializers.shopping_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_shopping_data(request,id):
    if request.method == "GET":
        data = shoppingmodel.objects.filter(Business_id=id)
        serializer = business_serializers.shopping_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    
@api_view(["POST"])
def shopping_update(request,id,shop_id):
    fs=FileSystemStorage
    # print(request.data)
    # print(request.FILES)
    shop_data = shoppingmodel.objects.get(Business_id=id,shop_id=shop_id)
    print(shop_data)
    shop_datas = shoppingmodel.objects.filter(Business_id=id,shop_id=shop_id).values()[0]
    print(shop_datas)

    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/shopping/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = shop_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/shopping/{id}/pan_file/"+pan_file,request.FILES["pan_file"])
        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = shop_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/shopping/{id}/profile/"+profile,request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = shop_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/shopping/{id}/bank_passbook/"+bank_passbook,request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = shop_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/shopping/{id}/gst_file/"+gst_file,request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = shop_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'door_number' : request.data['door_number'],
        'street_name' : request.data['street_name'],
        'area' : request.data['area'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.shopping_edit_serializer(instance=shop_data, data=data, partial=True)
    if dataserializer.is_valid():
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
# shop products
# .....electronics
@api_view(['POST'])
def shop_electronics(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_electronics/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_electronics/{id}/other_images/"+sav.name, sav) 
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
   
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price
    print(shop_products)

    db.shopelectronics.insert_one(shop_products)


    data= {
        'shop_id' : id,
        'product_id' : product_id,
        'status':False,
        
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_electronicsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def shop_get_adminelectronics(request):
    db = client['business']
    collection = db['shopelectronics']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_electronics(request,id):
    db = client['business']
    collection = db['shopelectronics']
    
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"False"})
    print(shop_product,"shop_product")
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_my_electronics(request,id,product_id):
    db = client['business']
    collection = db['shopelectronics']

    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"False","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    return JsonResponse(shop_products_json, safe=False)
 

@api_view(['POST'])
def shop_delete_electronics(request,id,product_id):
    db = client['business']

    db.shopelectronics.find_one({'shop_id':id,'product_id':product_id})

    db.shopelectronics.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])
def shop_update_electronics(request,id,product_id):
    db = client['business']
    collection = db['shopelectronics']
    shop_products = dict(request.POST)

    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_electronics/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths
    except:
        # shop_pro=collection.find_one({"shop_id": id,"product_id":product_id})
        # primary_image_paths=shop_pro.get("primary_image")
        # shop_products['primary_image'] = primary_image_paths
        pass
        
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_electronics/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    collection.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})
    return Response(id,status=status.HTTP_200_OK)

# shop_electorder model
@api_view(["POST","GET"])
def electorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopelectronics']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            elect_pro = dumps(alldata)
            print(type(elect_pro))
            return Response(elect_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)



# ....mobile
@api_view(['POST'])
def shop_mobile(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_mobile/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_mobile/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
            
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopmobile.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id,
    
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_mobileserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)



@api_view(['GET'])
def shop_get_mobile(request,id):
    db = client['business']
    collection = db['shopmobile']
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)





@api_view(['GET'])
def shop_get_adminmobile(request):
    db = client['business']
    collection = db['shopmobile']
   
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
    
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_my_mobile(request,id,product_id):
    db = client['business']
    collection = db['shopmobile']
   
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
 
    return JsonResponse(shop_products_json, safe=False)

@api_view(['POST'])
def shop_delete_mobile(request,id,product_id):
    db = client['business']

    #add

    db.shopmobile.find_one({'shop_id':id,'product_id':product_id})

    db.shopmobile.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])

def shop_update_mobile(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_mobile/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['other_images'] = other_imagelist

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_mobile/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopmobile.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})
    return Response(id,status=status.HTTP_200_OK)
# shop_mobileorder model
@api_view(["POST","GET"])
def mobileorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopmobile']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            mob_pro = dumps(alldata)
            print(type(mob_pro))
            return Response(mob_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ......furniture

@api_view(['POST'])
def shop_furniture(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_furniture/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_furniture/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopfurniture.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_furnitureserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])  
def shop_get_furniture(request,id):
    db = client['business']
    collection = db['shopfurniture']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_adminfurniture(request):
    db = client['business']
    collection = db['shopfurniture']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])  
def shop_get_my_furniture(request,id,product_id):
    db = client['business']
    collection = db['shopfurniture']
    
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)

    return JsonResponse(shop_products_json, safe=False)


@api_view(['POST'])
def shop_delete_furniture(request,id,product_id):
    db = client['business']

    #add
    db.shopfurniture.find_one({'shop_id':id,'product_id':product_id})
    db.shopfurniture.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_furniture(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_furniture/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:

        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_furniture/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopfurniture.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)
# shop_furnitureorder model
@api_view(["POST","GET"])
def furnitureorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopfurniture']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            fur_pro = dumps(alldata)
            print(type(fur_pro))
            return Response(fur_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# .......autoaccessories
@api_view(['POST'])
def shop_autoaccessories(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_autoaccessories/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_autoaccessories/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopautoaccessories.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_autoaccessoriesserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def shop_get_autoaccessories(request,id):
    db = client['business']
    collection = db['shopautoaccessories']
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_adminautoaccessories(request):
    db = client['business']
    collection = db['shopautoaccessories']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)


@api_view(['GET'])
def shop_get_my_autoaccessories(request,id,product_id):
    db = client['business']
    collection = db['shopautoaccessories']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)



@api_view(['POST'])
def shop_delete_autoaccessories(request,id,product_id):
    db = client['business']

    #add
    db.shopautoaccessories.find_one({'shop_id':id,'product_id':product_id})

    db.shopautoaccessories.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_autoaccessories(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:

        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_autoaccessories/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_autoaccessories/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopautoaccessories.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_accessoriesorder model
@api_view(["POST","GET"])
def accessoriesorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopautoaccessories']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            acc_pro = dumps(alldata)
            print(type(acc_pro))
            return Response(acc_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

# ........kitchen
@api_view(['POST'])
def shop_kitchen(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_kitchen/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_kitchen/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopkitchen.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_kitchenserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])    
def shop_get_kitchen(request,id):
    db = client['business']
    collection = db['shopkitchen']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_adminkitchen(request):
    db = client['business']
    collection = db['shopkitchen']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])    
def shop_get_my_kitchen(request,id,product_id):
    db = client['business']
    collection = db['shopkitchen']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['POST'])
def shop_delete_kitchen(request,id,product_id):
    db = client['business']

    db.shopkitchen.find_one({'shop_id':id,'product_id':product_id})

    db.shopkitchen.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_kitchen(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:

        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_kitchen/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
            
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_kitchen/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopkitchen.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_kitchenorder model
@api_view(["POST","GET"])
def kitchenorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopkitchen']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            kit_pro = dumps(alldata)
            print(type(kit_pro))
            return Response(kit_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

# ........fashion
@api_view(['POST'])
def shop_fashion(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_fashion/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_fashion/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopfashion.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_fashionserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])  
def shop_get_fashion(request,id):
    db = client['business']
    collection = db['shopfashion']
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_adminfashion(request):
    db = client['business']
    collection = db['shopfashion']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])  
def shop_get_my_fashion(request,id,product_id):
    db = client['business']
    collection = db['shopfashion']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['POST'])
def shop_delete_fashion(request,id,product_id):
    db = client['business']

    db.shopfashion.find_one({'shop_id':id,'product_id':product_id})

    db.shopfashion.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_fashion(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:

        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_fashion/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:

        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_fashion/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopfashion.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_fashionorder model
@api_view(["POST","GET"])
def fashionorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopfashion']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            fas_pro = dumps(alldata)
            print(type(fas_pro))
            return Response(fas_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

# ........appliances
@api_view(['POST'])
def shop_appliances(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_appliances/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_appliances/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopappliances.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_appliancesserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET']) 
def shop_get_appliances(request,id):
    db = client['business']
    collection = db['shopappliances']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_adminappliances(request):
    db = client['business']
    collection = db['shopappliances']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)


@api_view(['GET']) 
def shop_get_my_appliances(request,id,product_id):
    db = client['business']
    collection = db['shopappliances']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
    #delete
@api_view(['POST'])
def shop_delete_appliances(request,id,product_id):
    db = client['business']

    db.shopappliances.find_one({'shop_id':id,'product_id':product_id})

    db.shopappliances.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_appliances(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:

        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_appliances/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:

        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_appliances/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)
    db.shopappliances.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_appliancesorder model
@api_view(["POST","GET"])
def appliancesorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopappliances']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            app_pro = dumps(alldata)
            print(type(app_pro))
            return Response(app_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ........groceries
@api_view(['POST'])
def shop_groceries(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_groceries/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_groceries/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopgroceries.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_groceriesserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def shop_get_groceries(request,id):
    db = client['business']
    collection = db['shopgroceries']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_admingroceries(request):
    db = client['business']
    collection = db['shopgroceries']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_my_groceries(request,id,product_id):
    db = client['business']
    collection = db['shopgroceries']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
    #delete
@api_view(['POST'])
def shop_delete_groceries(request,id,product_id):
    db = client['business']

    #add
    db.shopgroceries.find_one({'shop_id':id,'product_id':product_id})

    db.shopgroceries.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_groceries(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_groceries/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_groceries/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)
    db.shopgroceries.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})
    return Response(id,status=status.HTTP_200_OK)


# shop_groceriesorder model
@api_view(["POST","GET"])
def groceriesorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopgroceries']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            gro_pro = dumps(alldata)
            print(type(gro_pro))
            return Response(gro_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ........petsupplies
@api_view(['POST'])
def shop_petsupplies(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_petsupplies/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_petsupplies/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shoppetsupplies.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_petsuppliesserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def shop_get_petsupplies(request,id):
    db = client['business']
    collection = db['shoppetsupplies']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_adminpetsupplies(request):
    db = client['business']
    collection = db['shoppetsupplies']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_my_petsupplies(request,id,product_id):
    db = client['business']
    collection = db['shoppetsupplies']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
    #delete
@api_view(['POST'])
def shop_delete_petsupplies(request,id,product_id):
    db = client['business']

    #add

    db.shoppetsupplies.find_one({'shop_id':id,'product_id':product_id})

    db.shoppetsupplies.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_petsupplies(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_petsupplies/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths
    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_petsupplies/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)
    db.shoppetsupplies.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})
    return Response(id,status=status.HTTP_200_OK)


# shop_petsuppliesorder model
@api_view(["POST","GET"])
def petsuppliesorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shoppetsupplies']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            pet_pro = dumps(alldata)
            print(type(pet_pro))
            return Response(pet_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# .......toys
@api_view(['POST'])
def shop_toys(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_toys/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_toys/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shoptoys.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_toysserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def shop_get_toys(request,id):
    db = client['business']
    collection = db['shoptoys']
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_admintoys(request):
    db = client['business']
    collection = db['shoptoys']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_my_toys(request,id,product_id):
    db = client['business']
    collection = db['shoptoys']
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['POST'])
def shop_delete_toys(request,id,product_id):
    db = client['business']
    #add

    db.shoptoys.find_one({'shop_id':id,'product_id':product_id})

    db.shoptoys.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_toys(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_toys/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_toys/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist
    except:
        pass
    shop_products = dict(request.POST)

    db.shoptoys.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_toysorder model
@api_view(["POST","GET"])
def toysorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shoptoys']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            shop_pro = dumps(alldata)
            print(type(shop_pro))
            return Response(shop_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ........sports
@api_view(['POST'])
def shop_sports(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_sports/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_sports/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))

        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopsports.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_sportsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])    
def shop_get_sports(request,id):
    db = client['business']
    collection = db['shopsports']
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)


@api_view(['GET'])
def shop_get_adminsports(request):
    db = client['business']
    collection = db['shopsports']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])    
def shop_get_my_sports(request,id,product_id):
    db = client['business']
    collection = db['shopsports']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
    #delete
@api_view(['POST'])
def shop_delete_sports(request,id,product_id):
    db = client['business']

    #add

    db.shopsports.find_one({'shop_id':id,'product_id':product_id})

    db.shopsports.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_sports(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_sports/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_sports/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopsports.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)


# shop_sportsorder model
@api_view(["POST","GET"])
def sportsorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopsports']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            sport_pro = dumps(alldata)
            return Response(sport_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ........healthcare
@api_view(['POST'])
def shop_healthcare(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_healthcare/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_healthcare/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shophealthcare.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_healthcareserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
def shop_get_adminhealthcare(request):
    db = client['business']
    collection = db['shophealthcare']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_healthcare(request,id):
    db = client['business']
    collection = db['shophealthcare']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])
def shop_get_my_healthcare(request,id,product_id):
    db = client['business']
    collection = db['shophealthcare']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
@api_view(['POST'])
def shop_delete_healthcare(request,id,product_id):
    db = client['business']

    db.shophealthcare.find_one({'shop_id':id,'product_id':product_id})

    db.shophealthcare.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_healthcare(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_healthcare/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_healthcare/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shophealthcare.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)


# shop_healthcareorder model
@api_view(["POST","GET"])
def healthcareorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shophealthcare']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            health_pro = dumps(alldata)
          
            return Response(health_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ........books
@api_view(['POST'])
def shop_books(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_books/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_books/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shopbooks.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_booksserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])    
def shop_get_books(request,id):
    db = client['business']
    collection = db['shopbooks']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_adminbooks(request):
    db = client['business']
    collection = db['shopbooks']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)
@api_view(['GET'])    
def shop_get_my_books(request,id,product_id):
    db = client['business']
    collection = db['shopbooks']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)
    #delete
@api_view(['POST'])
def shop_delete_books(request,id,product_id):
    db = client['business']

    #add

    db.shopbooks.find_one({'shop_id':id,'product_id':product_id})

    db.shopbooks.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_books(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_books/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_books/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist

    except:
        pass
    shop_products = dict(request.POST)

    db.shopbooks.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_booksorder model
@api_view(["POST","GET"])
def booksorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shopbooks']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            book_pro = dumps(alldata)
            return Response(book_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# ........personalcare
@api_view(['POST'])
def shop_personalcare(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/shop_personalcare/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/shop_personalcare/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    shop_products = dict(request.POST)
    shop_products['shop_id'] = id
    shop_products['product_id'] = product_id
    shop_products['primary_image'] = primary_image_paths
    shop_products['other_images'] = other_imagelist
    shop_products['selling_price'] = selling_price

    print(shop_products)
    db.shoppersonalcare.insert_one(shop_products)
    data={
        'shop_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.shop_personalcareserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def shop_get_personalcare(request,id):
    db = client['business']
    collection = db['shoppersonalcare']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True"})
    shop_products_list = list(shop_product)
    print(shop_products_list)

    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)


@api_view(['GET'])
def shop_get_adminpersonalcare(request):
    db = client['business']
    collection = db['shoppersonalcare']
    shop_products = collection.find({})
    
    shop_products_list = list(shop_products)
  
    shop_products_json = dumps(shop_products_list)
# # decode the shop_products
#     shop=loads(shop_products_json)
#     print(type(shop))
    
    return JsonResponse(shop_products_json, safe=False)

@api_view(['GET'])
def shop_get_my_personalcare(request,id,product_id):
    db = client['business']
    collection = db['shoppersonalcare']
 
    shop_product = collection.find({"shop_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    shop_products_list = list(shop_product)
    print(shop_products_list)
    shop_products_json = dumps(shop_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(shop_products_json, safe=False)

    #delete
@api_view(['POST'])
def shop_delete_personalcare(request,id,product_id):
    db = client['business']
    collection = db['shoppersonalcare']

    #add

    collection.find_one({'shop_id':id,'product_id':product_id})

    collection.delete_one({'shop_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def shop_update_personalcare(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/shop_personalcare/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        shop_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/shop_personalcare/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        shop_products['other_images'] = other_imagelist
    except:
        pass
   
    shop_products = dict(request.POST)

    db.shoppersonalcare.update_one({'shop_id':id,'product_id':product_id} ,{'$set':shop_products})

    return Response(id,status=status.HTTP_200_OK)

# shop_personalcareorder model
@api_view(["POST","GET"])
def personalcareorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.shop_ordermodel.objects.filter(Q(shop_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['shoppersonalcare']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            per_pro = dumps(alldata)
            
            return Response(per_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

# jewels_dashboard
    
@api_view(['GET'])
def jewel_total_revenue(request, id):
    if request.method == 'GET':
        total_revenue = models.jewel_ordermodel.objects.filter(jewel_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        jewel = models.jewellerymodel.objects.get(jewel_id=id)
        jewel.total_revenue = total_revenue
        jewel.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def jewel_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.jewel_ordermodel.objects.filter(jewel_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        jewel = models.jewellerymodel.objects.get(jewel_id=id)
        jewel.monthly_revenue = monthly_revenue
        jewel.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def jewel_orderstatus(request,id):
    if request.method == 'GET':

        jewel = models.jewel_ordermodel.objects.filter(jewel_id=id).first()
        if not jewel:
            return Response(data={'error': 'jewel not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.jewel_ordermodel.objects.filter(jewel_id=id, status='delivered').count()
        cancelled_count = models.jewel_ordermodel.objects.filter(jewel_id=id, status='cancelled').count()
        on_process_count = models.jewel_ordermodel.objects.filter(jewel_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def jewelproduct_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.jewel_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def jewelproduct_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.jewel_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def jewelproduct_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.jewel_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def jewel_all_products(request,id):
    if request.method== "GET":
        gol_data = models.jewel_goldmodel.objects.filter(jewel_id=id)
        sil_data = models.jewel_silvermodel.objects.filter(jewel_id=id)

        all_data = [
            gol_data, sil_data
        ]
       
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)


# jewellery
@api_view(['POST'])
def jewellery(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/jewellery/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/jewellery/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/jewellery/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/jewellery/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/jewellery/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    jewels_id=business_extension.jewel_id_generate()
    while True:
        if id == jewels_id:
            jewels_id=business_extension.jewel_id_generate()
        else:
            break

    data = {
        'Business_id': id,
        'jewel_id': jewels_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

        }

    print(data)
    basicdetailsserializer = business_serializers.jewellery_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['GET'])
def jewellery_alldata(request):
    if request.method == "GET":
        data = jewellerymodel.objects.all()
        serializer = business_serializers.jewellery_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
@api_view(['GET'])
def my_jewellery_data(request,id):
    if request.method == "GET":
        data = jewellerymodel.objects.get(jewel_id=id)
        print(data)
        serializer = business_serializers.jewellery_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_jewellery_data(request,id):
    if request.method == "GET":
        data = jewellerymodel.objects.filter(Business_id=id)
        serializer = business_serializers.jewellery_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def jewellery_update(request,id,jewel_id):
    fs=FileSystemStorage
    # print(id)
    # print(request.data)
    # print(request.FILES)
    jewel_data = jewellerymodel.objects.get(Business_id=id,jewel_id=jewel_id)
    print(jewel_data)
    jewel_datas = jewellerymodel.objects.filter(Business_id=id,jewel_id=jewel_id).values()[0]
    print(jewel_datas)
   
    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/jewellery/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = jewel_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/jewellery/{id}/pan_file/"+pan_file, request.FILES["pan_file"])

        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = jewel_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/jewellery/{id}/profile/"+profile, request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = jewel_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/jewellery/{id}/bank_passbook/"+bank_passbook, request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = jewel_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/jewellery/{id}/gst_file/"+gst_file, request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = jewel_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'door_number': request.data['door_number'],
        'street_name': request.data['street_name'],
        'area': request.data['area'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.jewellery_edit_serializer(instance=jewel_data, data=data, partial=True)
    if dataserializer.is_valid():
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

# jewellery products 
#....... gold 
@api_view(['POST'])
def jewel_gold(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/jewel_gold/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/jewel_gold/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    jewel_products = dict(request.POST)
    jewel_products['jewel_id'] = id
    jewel_products['product_id'] = product_id
    jewel_products['primary_image'] = primary_image_paths
    jewel_products['other_images'] = other_imagelist
    jewel_products['selling_price'] = selling_price

    print(jewel_products)
    db.jewelgold.insert_one(jewel_products)
    data={
        'jewel_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.jewel_goldserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def jewel_get_gold(request,id):
    db = client['business']
    collection = db['jewelgold']
 
    jewel_products = collection.find({"jewel_id": {"$regex":f"^{id}"},"status":"True"})
    jewel_products_list = list(jewel_products)
    print(jewel_products_list)

    jewel_products_json = dumps(jewel_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(jewel_products_json, safe=False)

@api_view(['GET'])
def jewel_get_admingold(request):
    db = client['business']
    collection = db['jewelgold']
    jewel_products = collection.find({})
    
    jewel_products_list = list(jewel_products)
  
    jewel_products_json = dumps(jewel_products_list)

    
    return JsonResponse(jewel_products_json, safe=False)

@api_view(['GET'])
def jewel_get_my_gold(request,id,product_id):
    db = client['business']
    collection = db['jewelgold']
 
    jewel_products = collection.find({"jewel_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    jewel_products_list = list(jewel_products)
    print(jewel_products_list)
    jewel_products_json = dumps(jewel_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(jewel_products_json, safe=False)

    #delete
@api_view(['POST'])
def jewel_delete_gold(request,id,product_id):
    db = client['business']

    db.jewelgold.find_one({'jewel_id':id,'product_id':product_id})

    db.jewelgold.delete_one({'jewel_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def jewel_update_gold(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/jewel_gold/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        jewel_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/jewel_gold/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        jewel_products['other_images'] = other_imagelist

    except:
        pass
    jewel_products = dict(request.POST)

    db.jewelgold.update_one({'jewel_id':id,'product_id':product_id} ,{'$set':jewel_products})

    return Response(id,status=status.HTTP_200_OK)


# jewelgoldorder model
@api_view(["POST","GET"])
def goldorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.jewel_ordermodel.objects.filter(Q(jewel_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['jewelgold']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            gold_pro = dumps(alldata)
            
            return Response(gold_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)

#...........silver 
@api_view(['POST'])
def jewel_silver(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/jewel_silver/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/jewel_silver/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    jewel_products = dict(request.POST)
    jewel_products['jewel_id'] = id
    jewel_products['product_id'] = product_id
    jewel_products['primary_image'] = primary_image_paths
    jewel_products['other_images'] = other_imagelist
    jewel_products['selling_price'] = selling_price

    print(jewel_products)
    db.jewelsilver.insert_one(jewel_products)
    data={
        'jewel_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.jewel_silverserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])    
def jewel_get_silver(request,id):
    db = client['business']
    collection = db['jewelsilver']
 
    jewel_products = collection.find({"jewel_id": {"$regex":f"^{id}"},"status":"True"})
    jewel_products_list = list(jewel_products)
    print(jewel_products_list)

    jewel_products_json = dumps(jewel_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(jewel_products_json, safe=False)

@api_view(['GET'])
def jewel_get_adminsilver(request):
    db = client['business']
    collection = db['jewelsilver']
    jewel_products = collection.find({})
    
    jewel_products_list = list(jewel_products)
  
    jewel_products_json = dumps(jewel_products_list)

    
    return JsonResponse(jewel_products_json, safe=False)

@api_view(['GET'])
def jewel_get_my_silver(request,id,product_id):
    db = client['business']
    collection = db['jewelsilver']
 
    jewel_products = collection.find({"jewel_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    jewel_products_list = list(jewel_products)
    print(jewel_products_list)
    jewel_products_json = dumps(jewel_products_list)
    # shop=loads(shop_products_json)
    # print(type(shop))
    # print(shop_product)
    return JsonResponse(jewel_products_json, safe=False)
    #delete
@api_view(['POST'])
def jewel_delete_silver(request,id,product_id):
    db = client['business']

    #add

    db.jewelsilver.find_one({'jewel_id':id,'product_id':product_id})

    db.jewelsilver.delete_one({'jewel_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def jewel_update_silver(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/jewel_silver/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        jewel_products['primary_image'] = primary_image_paths
    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/jewel_silver/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        jewel_products['other_images'] = other_imagelist

    except:
        pass
    jewel_products = dict(request.POST)

    db.jewelsilver.update_one({'jewel_id':id,'product_id':product_id} ,{'$set':jewel_products})

    return Response(id,status=status.HTTP_200_OK)

# jewel_silverorder model
@api_view(["POST","GET"])
def silverorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.jewel_ordermodel.objects.filter(Q(jewel_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['jewelsilver']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            sil_pro = dumps(alldata)
            
            return Response(sil_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
# food dashboard
    
@api_view(['GET'])
def food_total_revenue(request, id):
    if request.method == 'GET':
        total_revenue = models.food_ordermodel.objects.filter(food_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        food = models.foodmodel.objects.get(food_id=id)
        food.total_revenue = total_revenue
        food.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def food_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.food_ordermodel.objects.filter(food_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        food = models.foodmodel.objects.get(food_id=id)
        food.monthly_revenue = monthly_revenue
        food.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def food_orderstatus(request,id):
    if request.method == 'GET':

        food = models.food_ordermodel.objects.filter(food_id=id).first()
        if not food:
            return Response(data={'error': 'food not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.food_ordermodel.objects.filter(food_id=id, status='delivered').count()
        cancelled_count = models.food_ordermodel.objects.filter(food_id=id, status='cancelled').count()
        on_process_count = models.food_ordermodel.objects.filter(food_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def foodproduct_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.food_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def foodproduct_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.food_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def foodproduct_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.food_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def food_all_products(request,id):
    if request.method== "GET":
        tif_data = models.food_tiffenmodel.objects.filter(food_id=id)
        mea_data = models.food_mealsmodel.objects.filter(food_id=id)
        bir_data = models.food_biriyanimodel.objects.filter(food_id=id)        
        chic_data = models.food_chickenbiriyanimodel.objects.filter(food_id=id)
        bee_data = models.food_beefmodel.objects.filter(food_id=id)
        chi_data = models.food_chinesemodel.objects.filter(food_id=id)
        piz_data = models.food_pizzamodel.objects.filter(food_id=id)
        tea_data = models.food_teacoffemodel.objects.filter(food_id=id)
        ice_data = models.food_icecreammodel.objects.filter(food_id=id)
        fire_data = models.food_firedchickenmodel.objects.filter(food_id=id)        
        bur_data = models.food_burgermodel.objects.filter(food_id=id)
        cake_data = models.food_cakemodel.objects.filter(food_id=id)
        bak_data = models.food_bakerymodel.objects.filter(food_id=id)
        all_data = [
            tif_data, mea_data, bir_data, chic_data, bee_data,
            chi_data, piz_data, tea_data, ice_data, fire_data,
            bur_data, cake_data, bak_data
        ]
        # Calculate the total count
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)


#foodview  
@api_view(['POST'])
def food(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/food/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/food/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/food/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/food/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/food/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    foods_id=business_extension.food_id_generate()
    while True:
        if id == foods_id:
            foods_id=business_extension.food_id_generate()
        else:
            break

    data = {
        'Business_id': id,
        'food_id': foods_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],
        'fssa':request.POST['fssa'],
        'region':request.POST['region'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

        }

    print(data)
    basicdetailsserializer = business_serializers.food_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def food_alldata(request):
    if request.method == "GET":
        data = foodmodel.objects.all()
        serializer = business_serializers.food_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_food_data(request,id):
    if request.method == "GET":
        data = foodmodel.objects.get(food_id=id)
        print(data)
        serializer = business_serializers.food_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_food_data(request,id):
    if request.method == "GET":
        data = foodmodel.objects.filter(Business_id=id)
        serializer = business_serializers.food_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def food_update(request,id,food_id):
    fs=FileSystemStorage
    food_data = foodmodel.objects.get(Business_id=id,food_id=food_id)
    print(food_data)
    food_datas = foodmodel.objects.filter(Business_id=id,food_id=food_id).values()[0]
    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/food/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = food_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/food/{id}/pan_file/"+pan_file, request.FILES["pan_file"])

        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = food_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/food/{id}/profile/"+profile, request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = food_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/food/{id}/bank_passbook/"+bank_passbook, request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = food_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/food/{id}/gst_file/"+gst_file, request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = food_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'door_number' : request.data['door_number'],
        'street_name' : request.data['street_name'],
        'area' : request.data['area'],        
        'fssa' : request.data['fssa'],
        'region':request.data['region'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.food_edit_serializer(instance=food_data, data=data, partial=True)
    if dataserializer.is_valid():
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

# food products
# ......tiffen
@api_view(['POST'])
def food_tiffen(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_tiffen/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_tiffen/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodtiffen.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_tiffenserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET']) 
def food_get_tiffen(request,id):
    db = client['business']
    collection = db['foodtiffen']

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)

@api_view(['GET'])
def food_get_admintiffen(request):
    db = client['business']
    collection = db['foodtiffen']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)

@api_view(['GET']) 
def food_get_my_tiffen(request,id,product_id):
    db = client['business']
    collection = db['foodtiffen']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
@api_view(['POST'])
def food_delete_tiffen(request,id,product_id):
    db = client['business']

    #add

    db.foodtiffen.find_one({'food_id':id,'product_id':product_id})

    db.foodtiffen.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_tiffen(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_tiffen/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_tiffen/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodtiffen.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_tiffenorder model
@api_view(["POST","GET"])
def tiffenorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodtiffen']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            tif_pro = dumps(alldata)
            
            return Response(tif_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# .....meals
@api_view(['POST'])
def food_meals(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_meals/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_meals/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodmeals.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_mealsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def food_get_meals(request,id):
    db = client['business']
    collection = db['foodmeals']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)


@api_view(['GET'])
def food_get_adminmeals(request):
    db = client['business']
    collection = db['foodmeals']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)
@api_view(['GET']) 
def food_get_my_meals(request,id,product_id):
    db = client['business']
    collection = db['foodmeals']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_meals(request,id,product_id):
    db = client['business']

    #add

    db.foodmeals.find_one({'food_id':id,'product_id':product_id})

    db.foodmeals.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_meals(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_meals/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_meals/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodmeals.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_mealsorder model
@api_view(["POST","GET"])
def mealsorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodmeals']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            meal_pro = dumps(alldata)
            
            return Response(meal_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# ......biriyani
@api_view(['POST'])
def food_biriyani(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_biriyani/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_biriyani/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodbiriyani.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_biriyaniserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def food_get_biriyani(request,id):
    db = client['business']
    collection = db['foodbiriyani']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_adminbiriyani(request):
    db = client['business']
    collection = db['foodbiriyani']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)

@api_view(['GET']) 
def food_get_my_biriyani(request,id,product_id):
    db = client['business']
    collection = db['foodbiriyani']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)

    #delete
@api_view(['POST'])
def food_delete_biriyani(request,id,product_id):
    db = client['business']

    #add

    db.foodbiriyani.find_one({'food_id':id,'product_id':product_id})

    db.foodbiriyani.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_biriyani(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_biriyani/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_biriyani/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodbiriyani.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_biriyaniorder model
@api_view(["POST","GET"])
def biriyaniorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodbiriyani']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            bir_pro = dumps(alldata)
            
            return Response(bir_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# ......chickenbiriyani
@api_view(['POST'])
def food_chickenbiriyani(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_chickenbiriyani/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_chickenbiriyani/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodchickenbiriyani.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_chickenbiriyaniserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])  
def food_get_chickenbiriyani(request,id):
    db = client['business']
    collection = db['foodchickenbiriyani']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_adminchickenbiriyani(request):
    db = client['business']
    collection = db['foodchickenbiriyani']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)
@api_view(['GET']) 
def food_get_my_chickenbiriyani(request,id,product_id):
    db = client['business']
    collection = db['foodchickenbiriyani']
 
    food_product = collection.find_one({"food_id": id,"product_id":product_id})
    food_product.pop('_id')
    
    return JsonResponse(food_product)

    #delete
@api_view(['POST'])
def food_delete_chickenbiriyani(request,id,product_id):
    db = client['business']
    collection = db['foodchickenbiriyani']

    #add
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
@api_view(['POST'])
def food_update_chickenbiriyani(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_chickenbiriyani/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_chickenbiriyani/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodchickenbiriyani.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_chickenbiriyaniorder model
@api_view(["POST","GET"])
def chickenbiriyaniorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodchickenbiriyani']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            chik_pro = dumps(alldata)
            
            return Response(chik_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# ......beef
@api_view(['POST'])
def food_beef(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_beef/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_beef/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodbeef.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_beefserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
    
@api_view(['GET'])
def food_get_adminbeef(request):
    db = client['business']
    collection = db['foodbeef']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_beef(request,id):
    db = client['business']
    collection = db['foodbeef']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET']) 
def food_get_my_beef(request,id,product_id):
    db = client['business']
    collection = db['foodbeef']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_beef(request,id,product_id):
    db = client['business']

    #add

    db.foodbeef.find_one({'food_id':id,'product_id':product_id})

    db.foodbeef.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_beef(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_beef/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_beef/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodbeef.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)


#food_beeforder model
@api_view(["POST","GET"])
def beeforder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodbeef']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            beef_pro = dumps(alldata)
            
            return Response(beef_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# ......chinese
@api_view(['POST'])
def food_chinese(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_chinese/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_chinese/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodchinese.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_chineseserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def food_get_chinese(request,id):
    db = client['business']
    collection = db['foodchinese']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_adminchinese(request):
    db = client['business']
    collection = db['foodchinese']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)
@api_view(['GET']) 
def food_get_my_chinese(request,id,product_id):
    db = client['business']
    collection = db['foodchinese']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_chinese(request,id,product_id):
    db = client['business']
    collection = db['foodchinese']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    db.foodchinese.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_chinese(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_chinese/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_chinese/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodchinese.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_chineseorder model
@api_view(["POST","GET"])
def chineseorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodchinese']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            chin_pro = dumps(alldata)
            
            return Response(chin_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# .......pizza
@api_view(['POST'])
def food_pizza(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_pizza/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_pizza/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodpizza.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_pizzaserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def food_get_pizza(request,id):
    db = client['business']
    collection = db['foodpizza']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)

@api_view(['GET'])
def food_get_adminpizza(request):
    db = client['business']
    collection = db['foodpizza']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)

@api_view(['GET']) 
def food_get_my_pizza(request,id,product_id):
    db = client['business']
    collection = db['foodpizza']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)

    #delete
@api_view(['POST'])
def food_delete_pizza(request,id,product_id):
    db = client['business']
    #add

    db.foodpizza.find_one({'food_id':id,'product_id':product_id})

    db.foodpizza.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_pizza(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_pizza/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_pizza/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodpizza.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_pizzaorder model
@api_view(["POST","GET"])
def pizzaorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodpizza']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            piz_pro = dumps(alldata)
            
            return Response(piz_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# .......teacoffe
@api_view(['POST'])
def food_teacoffe(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_teacoffe/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_teacoffe/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodteacoffe.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_teacoffeserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def food_get_teacoffe(request,id):
    db = client['business']
    collection = db['foodteacoffe']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)


@api_view(['GET'])
def food_get_adminteacoffe(request):
    db = client['business']
    collection = db['foodteacoffe']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)


@api_view(['GET']) 
def food_get_my_teacoffe(request,id,product_id):
    db = client['business']
    collection = db['foodteacoffe']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_teacoffe(request,id,product_id):
    db = client['business']
    collection = db['foodteacoffe']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    collection.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_teacoffe(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_teacoffe/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_teacoffe/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodteacoffe.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_teacoffeorder model
@api_view(["POST","GET"])
def teacoffeorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodteacoffe']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            tea_pro = dumps(alldata)
            
            return Response(tea_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# .......icecream
@api_view(['POST'])
def food_icecream(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_icecream/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_icecream/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodicecream.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_icecreamserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def food_get_icecream(request,id):
    db = client['business']
    collection = db['foodicecream']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)

@api_view(['GET'])
def food_get_adminicecream(request):
    db = client['business']
    collection = db['foodicecream']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)


@api_view(['GET']) 
def food_get_my_icecream(request,id,product_id):
    db = client['business']
    collection = db['foodicecream']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)

    #delete
@api_view(['POST'])
def food_delete_icecream(request,id,product_id):
    db = client['business']
    collection = db['foodicecream']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    collection.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_icecream(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_icecream/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths
    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_icecream/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist
    except:
        pass
    food_products = dict(request.POST)

    db.foodpicecream.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)


#food_icecreamorder model
@api_view(["POST","GET"])
def icecreamorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodicecream']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            ice_pro = dumps(alldata)
            
            return Response(ice_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# .......firedchicken
@api_view(['POST'])
def food_firedchicken(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_firedchicken/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_firedchicken/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodfiredchicken.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_firedchickenserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def food_get_firedchicken(request,id):
    db = client['business']
    collection = db['foodfiredchicken']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)

@api_view(['GET'])
def food_get_adminfiredchicken(request):
    db = client['business']
    collection = db['foodfiredchicken']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)

@api_view(['GET']) 
def food_get_my_firedchicken(request,id,product_id):
    db = client['business']
    collection = db['foodfiredchicken']
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_firedchicken(request,id,product_id):
    db = client['business']
    collection = db['foodfiredchicken']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    collection.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_firedchicken(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_firedchicken/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_firedchicken/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodfiredchicken.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

#food_firedchickenorder model
@api_view(["POST","GET"])
def firedchickenorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodfiredchicken']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            fry_pro = dumps(alldata)
            
            return Response(fry_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
# .......burger
@api_view(['POST'])
def food_burger(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_burger/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_burger{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodburger.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_burgerserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def food_get_burger(request,id):
    db = client['business']
    collection = db['foodburger']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_adminburger(request):
    db = client['business']
    collection = db['foodburger']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)
@api_view(['GET']) 
def food_get_my_burger(request,id,product_id):
    db = client['business']
    collection = db['foodburger']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_burger(request,id,product_id):
    db = client['business']
    collection = db['foodburger']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    collection.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_burger(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_burger/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_burger/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodburger.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)


# food_burgerorder model
@api_view(["POST","GET"])
def burgerorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodburger']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            bur_pro = dumps(alldata)
            
            return Response(bur_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
#........cake
@api_view(['POST'])
def food_cake(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_cake/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_cake/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodcake.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_cakeserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def food_get_cake(request,id):
    db = client['business']
    collection = db['foodcake']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_admincake(request):
    db = client['business']
    collection = db['foodcake']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)

@api_view(['GET']) 
def food_get_my_cake(request,id,product_id):
    db = client['business']
    collection = db['foodcake']
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_cake(request,id,product_id):
    db = client['business']
    collection = db['foodcake']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    collection.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_cake(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_cake/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_cake/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodcake.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

# food_cakeorder model
@api_view(["POST","GET"])
def cakeorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodcake']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            cake_pro = dumps(alldata)
            
            return Response(cake_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  
#..... bakery
@api_view(['POST'])
def food_bakery(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/food_bakery/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/food_bakery/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    food_products = dict(request.POST)
    food_products['food_id'] = id
    food_products['product_id'] = product_id
    food_products['primary_image'] = primary_image_paths
    food_products['other_images'] = other_imagelist
    food_products['selling_price'] = selling_price

    print(food_products)
    db.foodbakery.insert_one(food_products)
    data={
        'food_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.food_bakeryserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def food_get_bakery(request,id):
    db = client['business']
    collection = db['foodbakery']
 

    food_product = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True"})
    food_product_list = list(food_product)
    print(food_product_list)

    food_product_json = dumps(food_product_list)

    return JsonResponse(food_product_json, safe=False)
@api_view(['GET'])
def food_get_adminbakery(request):
    db = client['business']
    collection = db['foodbakery']
    food_product = collection.find({})
    
    food_product_list = list(food_product)
  
    food_product_json = dumps(food_product_list)

    
    return JsonResponse(food_product_json, safe=False)
@api_view(['GET']) 
def food_get_my_bakery(request,id,product_id):
    db = client['business']
    collection = db['foodbakery']
 
    food_products = collection.find({"food_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    food_products_list = list(food_products)
    print(food_products_list)
    food_products_json = dumps(food_products_list)

    return JsonResponse(food_products_json, safe=False)
    #delete
@api_view(['POST'])
def food_delete_bakery(request,id,product_id):
    db = client['business']
    collection = db['foodbakery']

    #add

    collection.find_one({'food_id':id,'product_id':product_id})

    collection.delete_one({'food_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def food_update_bakery(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/food_bakery/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        food_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/food_bakery/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        food_products['other_images'] = other_imagelist

    except:
        pass
    food_products = dict(request.POST)

    db.foodbakery.update_one({'food_id':id,'product_id':product_id} ,{'$set':food_products})

    return Response(id,status=status.HTTP_200_OK)

#food_bakeryorder model
@api_view(["POST","GET"])
def bakeryorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.food_ordermodel.objects.filter(Q(food_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['foodbakery']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            bak_pro = dumps(alldata)
            
            return Response(bak_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)  

# freshcuts dashboard

@api_view(['GET'])
def fresh_total_revenue(request, id):

    if request.method == 'GET':
        total_revenue = models.fresh_ordermodel.objects.filter(fresh_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        fresh = models.freshcutsmodel.objects.get(fresh_id=id)
        fresh.total_revenue = total_revenue
        fresh.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def fresh_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.fresh_ordermodel.objects.filter(fresh_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        fresh = models.freshcutsmodel.objects.get(fresh_id=id)
        fresh.monthly_revenue = monthly_revenue
        fresh.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def fresh_orderstatus(request,id):
    if request.method == 'GET':

        shop = models.fresh_ordermodel.objects.filter(fresh_id=id).first()
        if not shop:
            return Response(data={'error': 'fresh not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.fresh_ordermodel.objects.filter(fresh_id=id, status='delivered').count()
        cancelled_count = models.fresh_ordermodel.objects.filter(fresh_id=id, status='cancelled').count()
        on_process_count = models.fresh_ordermodel.objects.filter(fresh_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def freshproduct_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.fresh_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def freshproduct_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.fresh_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def freshproduct_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.fresh_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def fresh_all_products(request,id):
    if request.method== "GET":
        chi_data = models.fresh_chickenmodel.objects.filter(fresh_id=id)
        mut_data = models.fresh_muttonmodel.objects.filter(fresh_id=id)
        bee_data = models.fresh_beefmodel.objects.filter(fresh_id=id)        
        fish_data = models.fresh_fishseafoodmodel.objects.filter(fresh_id=id)
        dry_data = models.fresh_dryfishmodel.objects.filter(fresh_id=id)
        pra_data = models.fresh_prawnsmodel.objects.filter(fresh_id=id)
        egg_data = models.fresh_eggmodel.objects.filter(fresh_id=id)
        pon_data = models.fresh_pondfishmodel.objects.filter(fresh_id=id)
        mea_data = models.fresh_meatmasalamodel.objects.filter(fresh_id=id)
        com_data = models.fresh_combomodel.objects.filter(fresh_id=id)        
        cho_data = models.fresh_choppedvegmodel.objects.filter(fresh_id=id)
        all_data = [
            chi_data, mut_data, bee_data, fish_data, dry_data,
            pra_data, egg_data, pon_data, mea_data, com_data,
            cho_data
        ]
        # Calculate the total count
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)



# freshcuts
@api_view(['POST'])
def freshcuts(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/freshcuts/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/freshcuts/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/freshcuts/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/freshcuts/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/freshcuts/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    freshcuts_id=business_extension.fresh_id_generate()
    while True:
        if id == freshcuts_id:
            freshcuts_id=business_extension.fresh_id_generate()
        else:
            break

    data = {
        'Business_id': id,
        'fresh_id': freshcuts_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],        
        'fssa':request.POST['fssa'],
        'region':request.POST['region'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

        }

    print(data)
    basicdetailsserializer = business_serializers.freshcuts_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def freshcuts_alldata(request):
    if request.method == "GET":
        data = freshcutsmodel.objects.all()
        serializer = business_serializers.freshcuts_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_freshcuts_data(request,id):
    if request.method == "GET":
        data = freshcutsmodel.objects.get(fresh_id=id)
        print(data)
        serializer = business_serializers.freshcuts_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_freshcuts_data(request,id):
    if request.method == "GET":
        data = freshcutsmodel.objects.filter(Business_id=id)
        serializer = business_serializers.freshcuts_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def freshcuts_update(request,id,fresh_id):
    fs=FileSystemStorage

    freshcuts_data = freshcutsmodel.objects.get(Business_id=id,fresh_id=fresh_id)
    print(freshcuts_data)
    freshcuts_datas = freshcutsmodel.objects.filter(Business_id=id,fresh_id=fresh_id).values()[0]

   
    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/freshcuts/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = freshcuts_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/freshcuts/{id}/pan_file/"+pan_file, request.FILES["pan_file"])

        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = freshcuts_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/freshcuts/{id}/profile/"+profile, request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = freshcuts_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/freshcuts/{id}/bank_passbook/"+bank_passbook, request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = freshcuts_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/freshcuts/{id}/gst_file/"+gst_file, request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = freshcuts_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'door_number' : request.data['door_number'],
        'street_name' : request.data['street_name'],
        'area' : request.data['area'],        
        'fssa' : request.data['fssa'],
        'region':request.data['region'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.freshcuts_edit_serializer(instance=freshcuts_data, data=data, partial=True)
    if dataserializer.is_valid():
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


# ......chicken
@api_view(['POST'])
def fresh_chicken(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_chicken/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_chicken/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['fresh_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshchicken.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_chickenserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def fresh_get_chicken(request,id):
    db = client['business']
    collection = db['freshchicken']

    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"False"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_adminchicken(request):
    db = client['business']
    collection = db['freshchicken']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_chicken(request,id,product_id):
    db = client['business']
    collection = db['freshchicken']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)
    #delete
@api_view(['POST'])
def fresh_delete_chicken(request,id,product_id):
    db = client['business']
    collection = db['freshchicken']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_chicken(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_chicken/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_chicken/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshchicken.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)



# fresh_chickenorder model
@api_view(["POST","GET"])
def chickenorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshchicken']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            chik_pro = dumps(alldata)
            
            return Response(chik_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........mutton
@api_view(['POST'])
def fresh_mutton(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_mutton/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_mutton/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshmutton.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_muttonserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
def fresh_get_mutton(request,id):
    db = client['business']
    collection = db['freshmutton']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_adminmutton(request):
    db = client['business']
    collection = db['freshmutton']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)

    
@api_view(['GET'])
def fresh_get_my_mutton(request,id,product_id):
    db = client['business']
    collection = db['freshmutton']
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)
    #delete
@api_view(['POST'])
def fresh_delete_mutton(request,id,product_id):
    db = client['business']
    collection = db['freshmutton']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_mutton(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_mutton/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_mutton/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshmutton.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)


# fresh_muttonorder model
@api_view(["POST","GET"])
def muttonorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshmutton']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            mut_pro = dumps(alldata)
            
            return Response(mut_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 

# .......beef
@api_view(['POST'])
def fresh_beef(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_beef/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_beef/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshbeef.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_beefserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
def fresh_get_beef(request,id):
    db = client['business']
    collection = db['freshbeef']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)

@api_view(['GET'])
def fresh_get_adminbeef(request):
    db = client['business']
    collection = db['freshbeef']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)


@api_view(['GET'])
def fresh_get_my_beef(request,id,product_id):
    db = client['business']
    collection = db['freshbeef']
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_beef(request,id,product_id):
    db = client['business']
    collection = db['freshbeef']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_beef(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_beef/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_beef/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshbeef.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)

# fresh_beeforder model
@api_view(["POST","GET"])
def beeforder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshbeef']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            beef_pro = dumps(alldata)
            
            return Response(beef_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........fishseafood
@api_view(['POST'])
def fresh_fishseafood(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_fishseafood/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_fishseafood/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshfishseafood.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_fishseafoodserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def fresh_get_fishseafood(request,id):
    db = client['business']
    collection = db['freshfishseafood']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_adminfishseafood(request):
    db = client['business']
    collection = db['freshfishseafood']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_fishseafood(request,id,product_id):
    db = client['business']
    collection = db['freshfishseafood']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_fishseafood(request,id,product_id):
    db = client['business']
    collection = db['freshfishseafood']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_fishseafood(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_fishseafood/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_fishseafood/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshfishseafood.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)


# fresh_fishseafoodorder model
@api_view(["POST","GET"])
def fishseafoodorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshfishseafood']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            fish_pro = dumps(alldata)
            
            return Response(fish_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........dryfish
@api_view(['POST'])
def fresh_dryfish(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_dryfish/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_dryfish/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshdryfish.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_dryfishserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def fresh_get_dryfish(request,id):
    db = client['business']
    collection = db['freshdryfish']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)


@api_view(['GET'])
def fresh_get_admindryfish(request):
    db = client['business']
    collection = db['freshdryfish']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_dryfish(request,id,product_id):
    db = client['business']
    collection = db['freshdryfish']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_dryfish(request,id,product_id):
    db = client['business']
    collection = db['freshdryfish']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_dryfish(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_dryfish/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_dryfish/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshdryfish.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)

# fresh_dryfishorder model
@api_view(["POST","GET"])
def dryfishorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshdryfish']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            dry_pro = dumps(alldata)
            
            return Response(dry_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........prawns
@api_view(['POST'])
def fresh_prawns(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_prawns/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_prawns/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshprawns.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_prawnsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def fresh_get_prawns(request,id):
    db = client['business']
    collection = db['freshprawns']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_adminprawns(request):
    db = client['business']
    collection = db['freshprawns']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_prawns(request,id,product_id):
    db = client['business']
    collection = db['freshprawns']
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)
    #delete
@api_view(['POST'])
def fresh_delete_prawns(request,id,product_id):
    db = client['business']
    collection = db['freshprawns']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_prawns(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_prawns/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_prawns/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist
    except:
        pass
    fresh_products = dict(request.POST)

    db.freshprawns.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)

# fresh_prawnsorder model
@api_view(["POST","GET"])
def prawnsorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshprawns']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            praw_pro = dumps(alldata)
            
            return Response(praw_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........egg
@api_view(['POST'])
def fresh_egg(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_egg/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_egg/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshegg.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_eggserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])   
def fresh_get_egg(request,id):
    db = client['business']
    collection = db['freshegg']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)


@api_view(['GET'])
def fresh_get_adminegg(request):
    db = client['business']
    collection = db['freshegg']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_egg(request,id,product_id):
    db = client['business']
    collection = db['freshegg']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_egg(request,id,product_id):
    db = client['business']
    collection = db['freshegg']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_egg(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_egg/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_egg/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
   
    fresh_products = dict(request.POST)

    db.freshegg.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)

# fresh_eggorder model
@api_view(["POST","GET"])
def eggorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshegg']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            egg_pro = dumps(alldata)
            
            return Response(egg_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........pond
@api_view(['POST'])
def fresh_pond(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_pond/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_pond/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshpond.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_pondfishserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def fresh_get_pond(request,id):
    db = client['business']
    collection = db['freshpond']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)


@api_view(['GET'])
def fresh_get_adminpond(request):
    db = client['business']
    collection = db['freshpond']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_pond(request,id,product_id):
    db = client['business']
    collection = db['freshpond']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_pond(request,id,product_id):
    db = client['business']
    collection = db['freshpond']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_pond(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_pond/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_pond/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshpond.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)


# fresh_pondorder model
@api_view(["POST","GET"])
def pondorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshpond']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            pond_pro = dumps(alldata)
            
            return Response(pond_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........meatmasala
@api_view(['POST'])
def fresh_meatmasala(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_meatmasala/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_meatmasala/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshmeatmasala.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_meatmasalaserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def fresh_get_meatmasala(request,id):
    db = client['business']
    collection = db['freshmeatmasala']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_adminmeatmasala(request):
    db = client['business']
    collection = db['freshmeatmasala']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_meatmasala(request,id,product_id):
    db = client['business']
    collection = db['freshmeatmasala']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_meatmasala(request,id,product_id):
    db = client['business']
    collection = db['freshmeatmasala']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_meatmasala(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_meatmasala/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_meatmasala/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshmeatmasala.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)


# fresh_meatmasalaorder model
@api_view(["POST","GET"])
def meatmasalaorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshmeatmasala']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            meat_pro = dumps(alldata)
            
            return Response(meat_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........combo
@api_view(['POST'])
def fresh_combo(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_combo/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_combo/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshcombo.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_comboserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET']) 
def fresh_get_combo(request,id):
    db = client['business']
    collection = db['freshcombo']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_admincombo(request):
    db = client['business']
    collection = db['freshcombo']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_combo(request,id,product_id):
    db = client['business']
    collection = db['freshcombo']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)

    #delete
@api_view(['POST'])
def fresh_delete_combo(request,id,product_id):
    db = client['business']
    collection = db['freshcombo']

    #add

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_combo(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_combo/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_combo/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshcombo.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)

# fresh_comboorder model
@api_view(["POST","GET"])
def comboorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshcombo']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            com_pro = dumps(alldata)
            
            return Response(com_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........choppedveg
@api_view(['POST'])
def fresh_choppedveg(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/fresh_choppedveg/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/fresh_choppedveg/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    fresh_products = dict(request.POST)
    fresh_products['food_id'] = id
    fresh_products['product_id'] = product_id
    fresh_products['primary_image'] = primary_image_paths
    fresh_products['other_images'] = other_imagelist
    fresh_products['selling_price'] = selling_price

    print(fresh_products)
    db.freshchoppedveg.insert_one(fresh_products)
    data={
        'fresh_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.fresh_choppedvegserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])  
def fresh_get_choppedveg(request,id):
    db = client['business']
    collection = db['freshchoppedveg']
 
    fresh_product = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True"})
    fresh_product_list = list(fresh_product)
    print(fresh_product_list)

    fresh_product_json = dumps(fresh_product_list)

    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_adminchoppedveg(request):
    db = client['business']
    collection = db['freshchoppedveg']
    fresh_product = collection.find({})
    
    fresh_product_list = list(fresh_product)
  
    fresh_product_json = dumps(fresh_product_list)

    
    return JsonResponse(fresh_product_json, safe=False)
@api_view(['GET'])
def fresh_get_my_choppedveg(request,id,product_id):
    db = client['business']
    collection = db['freshchoppedveg']
 
    fresh_products = collection.find({"fresh_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    fresh_products_list = list(fresh_products)
    print(fresh_products_list)
    fresh_products_json = dumps(fresh_products_list)

    return JsonResponse(fresh_products_json, safe=False)
    #delete
@api_view(['POST'])
def fresh_delete_choppedveg(request,id,product_id):
    db = client['business']
    collection = db['freshchoppedveg']

    collection.find_one({'fresh_id':id,'product_id':product_id})

    collection.delete_one({'fresh_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def fresh_update_choppedveg(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/fresh_choppedveg/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        fresh_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/fresh_choppedveg/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        fresh_products['other_images'] = other_imagelist

    except:
        pass
    fresh_products = dict(request.POST)

    db.freshchoppedveg.update_one({'fresh_id':id,'product_id':product_id} ,{'$set':fresh_products})

    return Response(id,status=status.HTTP_200_OK)
# fresh_choppedvegorder model
@api_view(["POST","GET"])
def choppedvegorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.fresh_ordermodel.objects.filter(Q(fresh_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['freshchoppedveg']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            chop_pro = dumps(alldata)
            
            return Response(chop_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 

# dailymio_dashboard
    
@api_view(['GET'])
def dmio_total_revenue(request, id):
    if request.method == 'GET':
        total_revenue = models.daily_ordermodel.objects.filter(dmio_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        dmio = models.dailymio_model.objects.get(dmio_id=id)
        dmio.total_revenue = total_revenue
        dmio.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def dmio_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.daily_ordermodel.objects.filter(dmio_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        dmio = models.dailymio_model.objects.get(dmio_id=id)
        dmio.monthly_revenue = monthly_revenue
        dmio.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def dmio_orderstatus(request,id):
    if request.method == 'GET':

        dmio = models.daily_ordermodel.objects.filter(dmio_id=id).first()
        if not dmio:
            return Response(data={'error': 'dmio not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.daily_ordermodel.objects.filter(dmio_id=id, status='delivered').count()
        cancelled_count = models.daily_ordermodel.objects.filter(dmio_id=id, status='cancelled').count()
        on_process_count = models.daily_ordermodel.objects.filter(dmio_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def dmioproduct_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.daily_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def dmioproduct_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.daily_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def dmioproduct_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.daily_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def dmio_all_products(request,id):
    if request.method== "GET":
        gro_data = models.dmio_grocerymodel.objects.filter(dmio_id=id)
        meat_data = models.dmio_meatmodel.objects.filter(dmio_id=id)
        fish_data = models.dmio_fishmodel.objects.filter(dmio_id=id)        
        eggs_data = models.dmio_eggsmodel.objects.filter(dmio_id=id)
        fru_data = models.dmio_fruitsmodel.objects.filter(dmio_id=id)
        veg_data = models.dmio_vegitablesmodel.objects.filter(dmio_id=id)
        dair_data = models.dmio_dairymodel.objects.filter(dmio_id=id)
        all_data = [
            gro_data, meat_data, fish_data, eggs_data,
            fru_data, veg_data, dair_data
        ]
        # Calculate the total count
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)


# dailymio_model

@api_view(['POST'])
def dailymio(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/dailymio/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/dailymio/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/dailymio/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/dailymio/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/dailymio/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    dmio_id=business_extension.dmio_id_generate()
    while True:
        if id == dmio_id:
            dmio_id=business_extension.dmio_id_generate()
        else:
            break

    data = {
        'Business_id': id,
        'dmio_id':dmio_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],        
        'fssa':request.POST['fssa'],
        'region':request.POST['region'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

        }

    print(data)
    basicdetailsserializer = business_serializers.dailymio_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def dailymio_alldata(request):
    if request.method == "GET":
        data = dailymio_model.objects.all()
        serializer = business_serializers.dailymio_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_dailymio_data(request,id):
    if request.method == "GET":
        data = dailymio_model.objects.get(dmio_id=id)
        print(data)
        serializer = business_serializers.dailymio_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_dailymio_data(request,id):
    if request.method == "GET":
        data = dailymio_model.objects.filter(Business_id=id)
        serializer = business_serializers.dailymio_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def dailymio_update(request,id,dmio_id):
    fs=FileSystemStorage

    dailymio_data = dailymio_model.objects.get(Business_id=id,dmio_id=dmio_id)
    print(dailymio_data)
    dailymio_datas = dailymio_model.objects.filter(Business_id=id,dmio_id=dmio_id).values()[0]

   
    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/dailymio/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = dailymio_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/dailymio/{id}/pan_file/"+pan_file, request.FILES["pan_file"])

        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = dailymio_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/dailymio/{id}/profile/"+profile, request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = dailymio_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/dailymio/{id}/bank_passbook/"+bank_passbook, request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = dailymio_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/dailymio/{id}/gst_file/"+gst_file, request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = dailymio_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'door_number' : request.data['door_number'],
        'street_name' : request.data['street_name'],
        'area' : request.data['area'],        
        'fssa' : request.data["fssa"],
        'region':request.data['region'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.dailymio_edit_serializer(instance=dailymio_data, data=data, partial=True)
    if dataserializer.is_valid():
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
# dailymio products
# .......grocery

@api_view(['POST'])
def dmio_grocery(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_grocery/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_grocery/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price

    print(dmio_products)
    db.dmiogrocery.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_groceryserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def dmio_get_grocery(request,id):
    db = client['business']
    collection = db['dmiogrocery']
 
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_admingrocery(request):
    db = client['business']
    collection = db['dmiogrocery']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_my_grocery(request,id,product_id):
    db = client['business']
    collection = db['dmiogrocery']
 
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)
    #delete
@api_view(['POST'])
def dmio_delete_grocery(request,id,product_id):
    db = client['business']
    collection = db['dmiogrocery']

    #add

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def dmio_update_grocery(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_grocery/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_grocery/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass
   
    dmio_products = dict(request.POST)
    db.dmiogrocery.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)


# dmio_groceryorder model
@api_view(["POST","GET"])
def groceryorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmiogrocery']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            gro_pro = dumps(alldata)
            
            return Response(gro_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# .......meat
@api_view(['POST'])
def dmio_meat(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_meat/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_meat/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price

    print(dmio_products)
    db.dmiomeat.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_meatserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])  
def dmio_get_meat(request,id):
    db = client['business']
    collection = db['dmiomeat']
 
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)



@api_view(['GET'])
def dmio_get_adminmeat(request):
    db = client['business']
    collection = db['dmiomeat']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)
@api_view(['GET'])
def dmio_get_my_meat(request,id,product_id):
    db = client['business']
    collection = db['dmiomeat']
 
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)
    #delete
@api_view(['POST'])
def dmio_delete_meat(request,id,product_id):
    db = client['business']
    collection = db['dmiomeat']

    #add

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def dmio_update_meat(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_meat/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_meat/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass
    dmio_products = dict(request.POST)

    db.dmiomeat.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)



# dmio_meatorder model
@api_view(["POST","GET"])
def meatorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmiomeat']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            met_pro = dumps(alldata)
            
            return Response(met_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# .......fish
@api_view(['POST'])
def dmio_fish(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_fish/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_fish/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price


    print(dmio_products)
    db.dmiofish.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_fishserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])   
def dmio_get_fish(request,id):
    db = client['business']
    collection = db['dmiofish']
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_adminfish(request):
    db = client['business']
    collection = db['dmiofish']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_my_fish(request,id,product_id):
    db = client['business']
    collection = db['dmiofish']
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)

    #delete
@api_view(['POST'])
def dmio_delete_fish(request,id,product_id):
    db = client['business']
    collection = db['dmiofish']

    #add

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def dmio_update_fish(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_fish/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_fish/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass

    dmio_products = dict(request.POST)

    db.dmiofish.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)

# dmio_fishorder model
@api_view(["POST","GET"])
def fishorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmiofish']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            fis_pro = dumps(alldata)
            
            return Response(fis_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ........eggs
@api_view(['POST'])
def dmio_eggs(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_eggs/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_eggs/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price


    print(dmio_products)
    db.dmioeggs.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_eggsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
def dmio_get_eggs(request,id):
    db = client['business']
    collection = db['dmioeggs']
 
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_admineggs(request):
    db = client['business']
    collection = db['dmioeggs']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_my_eggs(request,id,product_id):
    db = client['business']
    collection = db['dmioeggs']
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)

    #delete
@api_view(['POST'])
def dmio_delete_eggs(request,id,product_id):
    db = client['business']
    collection = db['dmioeggs']

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def dmio_update_eggs(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_eggs/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_eggs/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass
    dmio_products = dict(request.POST)

    db.dmioeggs.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)

# dmio_eggsorder model
@api_view(["POST","GET"])
def eggsorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmioeggs']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            egg_pro = dumps(alldata)
            
            return Response(egg_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ....fruits
@api_view(['POST'])
def dmio_fruits(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_fruits/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_fruits/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price

    print(dmio_products)
    db.dmiofruits.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_fruitsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def dmio_get_fruits(request,id):
    db = client['business']
    collection = db['dmiofruits']
 
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)



@api_view(['GET'])
def dmio_get_adminfruits(request):
    db = client['business']
    collection = db['dmiofruits']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)
@api_view(['GET'])
def dmio_get_my_fruits(request,id,product_id):
    db = client['business']
    collection = db['dmiofruits']
 
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)
    #delete
@api_view(['POST'])
def dmio_delete_fruits(request,id,product_id):
    db = client['business']
    collection = db['dmiofruits']

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def dmio_update_fruits(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_fruits/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:

        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_fruits/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass
    dmio_products = dict(request.POST)

    db.dmiofruits.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)


# dmio_fruitsorder model
@api_view(["POST","GET"])
def fruitsorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmiofruits']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            fru_pro = dumps(alldata)
            
            return Response(fru_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ......vegitables
@api_view(['POST'])
def dmio_vegitables(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_vegitables/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_vegitables/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price

    print(dmio_products)
    db.dmiovegitables.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_vegitablesserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def dmio_get_vegitables(request,id):
    db = client['business']
    collection = db['dmiovegitables']
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)


@api_view(['GET'])
def dmio_get_adminvegitables(request):
    db = client['business']
    collection = db['dmiovegitables']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)


@api_view(['GET'])
def dmio_get_my_vegitables(request,id,product_id):
    db = client['business']
    collection = db['dmiovegitables']
 
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)
    #delete
@api_view(['POST'])
def dmio_delete_vegitables(request,id,product_id):
    db = client['business']
    collection = db['dmiovegitables']

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def dmio_update_vegitables(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_vegitables/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_vegitables/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass
    dmio_products = dict(request.POST)

    db.dmiovegitables.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)

# dmio_vegitablesorder model
@api_view(["POST","GET"])
def vegitablesorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmiovegitables']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            veg_pro = dumps(alldata)
            
            return Response(veg_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 

# ........dairy
@api_view(['POST'])
def dmio_dairy(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/dmio_dairy/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/dmio_dairy/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    dmio_products = dict(request.POST)
    dmio_products['dmio_id'] = id
    dmio_products['product_id'] = product_id
    dmio_products['primary_image'] = primary_image_paths
    dmio_products['other_images'] = other_imagelist
    dmio_products['selling_price'] = selling_price

    print(dmio_products)
    db.dmiodairy.insert_one(dmio_products)
    data={
        'dmio_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.dmio_dairyserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def dmio_get_dairy(request,id):
    db = client['business']
    collection = db['dmiodairy']
    dmio_product = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True"})
    dmio_product_list = list(dmio_product)
    print(dmio_product_list)

    dmio_product_json = dumps(dmio_product_list)

    return JsonResponse(dmio_product_json, safe=False)


@api_view(['GET'])
def dmio_get_admindairy(request):
    db = client['business']
    collection = db['dmiodairy']
    dmio_product = collection.find({})
    
    dmio_product_list = list(dmio_product)
  
    dmio_product_json = dumps(dmio_product_list)

    
    return JsonResponse(dmio_product_json, safe=False)

@api_view(['GET'])
def dmio_get_my_dairy(request,id,product_id):
    db = client['business']
    collection = db['dmiodairy']
 
    dmio_products = collection.find({"dmio_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    dmio_products_list = list(dmio_products)
    print(dmio_products_list)
    dmio_products_json = dumps(dmio_products_list)

    return JsonResponse(dmio_products_json, safe=False)

    #delete
@api_view(['POST'])
def dmio_delete_dairy(request,id,product_id):
    db = client['business']
    collection = db['dmiodairy']

    #add

    collection.find_one({'dmio_id':id,'product_id':product_id})

    collection.delete_one({'dmio_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)

@api_view(['POST'])
def dmio_update_dairy(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/dmio_dairy/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        dmio_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/dmio_dairy/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        dmio_products['other_images'] = other_imagelist

    except:
        pass
    dmio_products = dict(request.POST)

    db.dmiodairy.update_one({'dmio_id':id,'product_id':product_id} ,{'$set':dmio_products})

    return Response(id,status=status.HTTP_200_OK)


# dmio_dairyorder model
@api_view(["POST","GET"])
def dairyorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.daily_ordermodel.objects.filter(Q(dmio_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['dmiodairy']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            dar_pro = dumps(alldata)
            
            return Response(dar_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 


# pharmacy _dashboard
   
@api_view(['GET'])
def pharmacy_total_revenue(request, id):
    if request.method == 'GET':
        total_revenue = models.pharmacy_ordermodel.objects.filter(pharm_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        pharm = models.pharmacy_model.objects.get(pharm_id=id)
        pharm.total_revenue = total_revenue
        pharm.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def pharm_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.pharmacy_ordermodel.objects.filter(pharm_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        pharm = models.pharmacy_model.objects.get(pharm_id=id)
        pharm.monthly_revenue = monthly_revenue
        pharm.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def pharm_orderstatus(request,id):
    if request.method == 'GET':

        pharm = models.pharmacy_ordermodel.objects.filter(pharm_id=id).first()
        if not pharm:
            return Response(data={'error': 'pharm not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.shop_ordermodel.objects.filter(pharm_id=id, status='delivered').count()
        cancelled_count = models.shop_ordermodel.objects.filter(pharm_id=id, status='cancelled').count()
        on_process_count = models.shop_ordermodel.objects.filter(pharm_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def pharmproduct_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.pharmacy_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def pharmproduct_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.pharmacy_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def pharmproduct_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.pharmacy_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pharm_all_products(request,id):
    if request.method== "GET":
        allo_data = models.pharmacy_allopathicmodel.objects.filter(pharm_id=id)
        ayur_data = models.pharmacy_ayurvedicmodel.objects.filter(pharm_id=id)
        sidd_data = models.pharmacy_siddhamodel.objects.filter(pharm_id=id)        
        unani_data = models.pharmacy_unanimodel.objects.filter(pharm_id=id)
        herb_data = models.pharmacy_herbaldrinksmodel.objects.filter(pharm_id=id)

        all_data = [
            allo_data, ayur_data, sidd_data, unani_data, herb_data
        ]
        # Calculate the total count
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)

# pharmacy_model
@api_view(['POST'])
def pharmacy(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/pharmacy/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/pharmacy/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/pharmacy/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/pharmacy/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/pharmacy/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    pharms_id=business_extension.pharm_id_generate()
    while True:
        if id == pharms_id:
            pharms_id=business_extension.pharm_id_generate()
        else:
            break
    data = {
        'Business_id': id,
        'pharm_id': pharms_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],        
        'fssa':request.POST['fssa'],
        'region':request.POST['region'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

        }

    print(data)
    basicdetailsserializer = business_serializers.pharmacy_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def pharmacy_alldata(request):
    if request.method == "GET":
        data = pharmacy_model.objects.all()
        serializer = business_serializers.pharmacy_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_pharmacy_data(request,id):
    if request.method == "GET":
        data = pharmacy_model.objects.get(pharm_id=id)
        print(data)
        serializer = business_serializers.pharmacy_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def business_pharmacy_data(request,id):
    if request.method == "GET":
        data = pharmacy_model.objects.filter(Business_id=id)
        serializer = business_serializers.pharmacy_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


@api_view(["POST"])
def pharmacy_update(request,id,pharm_id):
    fs=FileSystemStorage

    pharmacy_data = pharmacy_model.objects.get(Business_id=id,pharm_id=pharm_id)
    print(pharmacy_data)
    pharmacy_datas = pharmacy_model.objects.filter(Business_id=id,pharm_id=pharm_id).values()[0]

    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/pharmacy/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = pharmacy_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/pharmacy/{id}/pan_file/"+pan_file, request.FILES["pan_file"])

        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = pharmacy_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/pharmacy/{id}/profile/"+profile, request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = pharmacy_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/pharmacy/{id}/bank_passbook/"+bank_passbook, request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = pharmacy_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/pharmacy/{id}/gst_file/"+gst_file, request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = pharmacy_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'door_number' : request.data['door_number'],
        'street_name' : request.data['street_name'],
        'area' : request.data['area'],
        'fssa':request.data['fssa'],
        'region':request.data['region'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.pharmacy_edit_serializer(instance=pharmacy_data, data=data, partial=True)
    if dataserializer.is_valid():
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


# pharmacy products
# ....allopathic
@api_view(['POST'])
def pharmacy_allopathic(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/pharmacy_allopathic/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/pharmacy_allopathic/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    pharmacy_products = dict(request.POST)
    pharmacy_products['pharm_id'] = id
    pharmacy_products['product_id'] = product_id
    pharmacy_products['primary_image'] = primary_image_paths
    pharmacy_products['other_images'] = other_imagelist
    pharmacy_products['selling_price'] = selling_price

    print(pharmacy_products)
    db.pharmacyallopathic.insert_one(pharmacy_products)
    data={
        'pharm_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.pharmacy_allopathicserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])
def pharmacy_get_allopathic(request,id):
    db = client['business']
    collection = db['pharmacyallopathic']
 
    pharmacy_product = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True"})
    pharmacy_product_list = list(pharmacy_product)
    print(pharmacy_product_list)

    pharmacy_product_json = dumps(pharmacy_product_list)

    return JsonResponse(pharmacy_product_json, safe=False)

@api_view(['GET'])
def pharmacy_get_adminallopathic(request):
    db = client['business']
    collection = db['pharmacyallopathic']
    pharmacy_product = collection.find({})
    
    pharmacy_product_list = list(pharmacy_product)
  
    pharmacy_product_json = dumps(pharmacy_product_list)

    
    return JsonResponse(pharmacy_product_json, safe=False)
@api_view(['GET'])
def pharmacy_get_my_allopathic(request,id,product_id):
    db = client['business']
    collection = db['pharmacyallopathic']
 
    pharmacy_products = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    pharmacy_products_list = list(pharmacy_products)
    print(pharmacy_products_list)
    pharmacy_products_json = dumps(pharmacy_products_list)

    return JsonResponse(pharmacy_products_json, safe=False)
    #delete
@api_view(['POST'])
def pharmacy_delete_allopathic(request,id,product_id):
    db = client['business']
    collection = db['pharmacyallopathic']

    #add

    collection.find_one({'pharm_id ':id,'product_id':product_id})

    collection.delete_one({'pharm_id ':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def pharmacy_update_allopathic(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/pharmacy_allopathic/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        pharmacy_products['primary_image'] = primary_image_paths

    except:
        pass
    try:

        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/pharmacy_allopathic/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        pharmacy_products['other_images'] = other_imagelist

    except:
        pass
    pharmacy_products = dict(request.POST)

    db.pharmacyallopathic.update_one({'pharm_id':id,'product_id':product_id} ,{'$set':pharmacy_products})

    return Response(id,status=status.HTTP_200_OK)


# pharmacy_allopathicorder model
@api_view(["POST","GET"])
def allopathicorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.pharmacy_ordermodel.objects.filter(Q(pharm_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['pharmacyallopathic']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            allo_pro = dumps(alldata)
            
            return Response(allo_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# .....ayurvedic
@api_view(['POST'])
def pharmacy_ayurvedic(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/pharmacy_ayurvedic/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/pharmacy_ayurvedic/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    pharmacy_products = dict(request.POST)
    pharmacy_products['pharm_id'] = id
    pharmacy_products['product_id'] = product_id
    pharmacy_products['primary_image'] = primary_image_paths
    pharmacy_products['other_images'] = other_imagelist
    pharmacy_products['selling_price'] = selling_price

    print(pharmacy_products)
    db.pharmacyayurvedic.insert_one(pharmacy_products)
    data={
        'pharm_id ' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.pharmacy_ayurvedicserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])    
def pharmacy_get_ayurvedic(request,id):
    db = client['business']
    collection = db['pharmacyayurvedic']
    pharmacy_product = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True"})
    pharmacy_product_list = list(pharmacy_product)
    print(pharmacy_product_list)

    pharmacy_product_json = dumps(pharmacy_product_list)

    return JsonResponse(pharmacy_product_json, safe=False)
@api_view(['GET'])
def pharmacy_get_adminayurvedic(request):
    db = client['business']
    collection = db['pharmacyayurvedic']
    pharmacy_product = collection.find({})
    
    pharmacy_product_list = list(pharmacy_product)
  
    pharmacy_product_json = dumps(pharmacy_product_list)

    
    return JsonResponse(pharmacy_product_json, safe=False)


@api_view(['GET'])    
def pharmacy_get_my_ayurvedic(request,id,product_id):
    db = client['business']
    collection = db['pharmacyayurvedic']
 
    pharmacy_products = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    pharmacy_products_list = list(pharmacy_products)
    print(pharmacy_products_list)
    pharmacy_products_json = dumps(pharmacy_products_list)

    return JsonResponse(pharmacy_products_json, safe=False)
    #delete
@api_view(['POST'])
def pharmacy_delete_ayurvedic(request,id,product_id):
    db = client['business']
    collection = db['pharmacyayurvedic']

    #add

    collection.find_one({'pharm_id':id,'product_id':product_id})

    collection.delete_one({'pharm_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def pharmacy_update_ayurvedic(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/pharmacy_ayurvedic/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        pharmacy_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/pharmacy_ayurvedic/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        pharmacy_products['other_images'] = other_imagelist

    except:
        pass
    pharmacy_products = dict(request.POST)

    db.pharmacyayurvedic.update_one({'pharm_id':id,'product_id':product_id} ,{'$set':pharmacy_products})

    return Response(id,status=status.HTTP_200_OK)

# pharmacy_ayurvedicorder model
@api_view(["POST","GET"])
def ayurvedicorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.pharmacy_ordermodel.objects.filter(Q(pharm_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['pharmacyayurvedic']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            ayur_pro = dumps(alldata)
            
            return Response(ayur_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# .....siddha
@api_view(['POST'])
def pharmacy_siddha(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/pharmacy_siddha/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/pharmacy_siddha/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    pharmacy_products = dict(request.POST)
    pharmacy_products['pharm_id'] = id
    pharmacy_products['product_id'] = product_id
    pharmacy_products['primary_image'] = primary_image_paths
    pharmacy_products['other_images'] = other_imagelist
    pharmacy_products['selling_price'] = selling_price

    print(pharmacy_products)
    db.pharmacysiddha.insert_one(pharmacy_products)
    data={
        'pharm_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.pharmacy_siddhaserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])   
def pharmacy_get_siddha(request,id):
    db = client['business']
    collection = db['pharmacysiddha']
    pharmacy_product = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True"})
    pharmacy_product_list = list(pharmacy_product)
    print(pharmacy_product_list)

    pharmacy_product_json = dumps(pharmacy_product_list)

    return JsonResponse(pharmacy_product_json, safe=False)
@api_view(['GET'])
def pharmacy_get_adminsiddha(request):
    db = client['business']
    collection = db['pharmacysiddha']
    pharmacy_product = collection.find({})
    
    pharmacy_product_list = list(pharmacy_product)
  
    pharmacy_product_json = dumps(pharmacy_product_list)

    
    return JsonResponse(pharmacy_product_json, safe=False)

@api_view(['GET'])   
def pharmacy_get_my_siddha(request,id,product_id):
    db = client['business']
    collection = db['pharmacysiddha']
 
    pharmacy_products = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    pharmacy_products_list = list(pharmacy_products)
    print(pharmacy_products_list)
    pharmacy_products_json = dumps(pharmacy_products_list)

    return JsonResponse(pharmacy_products_json, safe=False)
    #delete
@api_view(['POST'])
def pharmacy_delete_siddha(request,id,product_id):
    db = client['business']
    collection = db['pharmacysiddha']

    #add

    collection.find_one({'pharm_id':id,'product_id':product_id})

    collection.delete_one({'pharm_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def pharmacy_update_siddha(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/pharmacy_siddha/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        pharmacy_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/pharmacy_siddha/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        pharmacy_products['other_images'] = other_imagelist

    except:
        pass
    pharmacy_products = dict(request.POST)

    db.pharmacysiddha.update_one({'pharm_id':id,'product_id':product_id} ,{'$set':pharmacy_products})

    return Response(id,status=status.HTTP_200_OK)

# pharmacy_siddhaorder model
@api_view(["POST","GET"])
def siddhaorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.pharmacy_ordermodel.objects.filter(Q(pharm_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['pharmacysiddha']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            sid_pro = dumps(alldata)
            
            return Response(sid_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# ......unani
@api_view(['POST'])
def pharmacy_unani(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/pharmacy_unani/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/pharmacy_unani/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    pharmacy_products = dict(request.POST)
    pharmacy_products['pharm_id'] = id
    pharmacy_products['product_id'] = product_id
    pharmacy_products['primary_image'] = primary_image_paths
    pharmacy_products['other_images'] = other_imagelist
    pharmacy_products['selling_price'] = selling_price

    print(pharmacy_products)
    db.pharmacyunani.insert_one(pharmacy_products)
    data={
        'pharm_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.pharmacy_unaniserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])  
def pharmacy_get_unani(request,id):
    db = client['business']
    collection = db['pharmacyunani']
 
    pharmacy_product = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True"})
    pharmacy_product_list = list(pharmacy_product)
    print(pharmacy_product_list)

    pharmacy_product_json = dumps(pharmacy_product_list)

    return JsonResponse(pharmacy_product_json, safe=False)

@api_view(['GET'])
def pharmacy_get_adminunani(request):
    db = client['business']
    collection = db['pharmacyunani']
    pharmacy_product = collection.find({})
    
    pharmacy_product_list = list(pharmacy_product)
  
    pharmacy_product_json = dumps(pharmacy_product_list)

    
    return JsonResponse(pharmacy_product_json, safe=False)

@api_view(['GET'])  
def pharmacy_get_my_unani(request,id,product_id):
    db = client['business']
    collection = db['pharmacyunani']
 
    pharmacy_products = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    pharmacy_products_list = list(pharmacy_products)
    print(pharmacy_products_list)
    pharmacy_products_json = dumps(pharmacy_products_list)

    return JsonResponse(pharmacy_products_json, safe=False)
    #delete
@api_view(['POST'])
def pharmacy_delete_unani(request,id,product_id):
    db = client['business']
    collection = db['pharmacyunani']


    collection.find_one({'pharm_id':id,'product_id':product_id})

    collection.delete_one({'pharm_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def pharmacy_update_unani(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/pharmacy_unani/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        pharmacy_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/pharmacy_unani/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        pharmacy_products['other_images'] = other_imagelist

    except:
        pass
    pharmacy_products = dict(request.POST)

    db.pharmacyunani.update_one({'pharm_id':id,'product_id':product_id} ,{'$set':pharmacy_products})

    return Response(id,status=status.HTTP_200_OK)

# pharmacy_unaniorder model
@api_view(["POST","GET"])
def unaniorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.pharmacy_ordermodel.objects.filter(Q(pharm_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['pharmacyunani']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            una_pro = dumps(alldata)
            
            return Response(una_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 
# .......herbaldrinks
@api_view(['POST'])
def pharmacy_herbaldrinks(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/pharmacy_herbaldrinks/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/pharmacy_herbaldrinks/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    pharmacy_products = dict(request.POST)
    pharmacy_products['pharm_id'] = id
    pharmacy_products['product_id'] = product_id
    pharmacy_products['primary_image'] = primary_image_paths
    pharmacy_products['other_images'] = other_imagelist
    pharmacy_products['selling_price'] = selling_price

    print(pharmacy_products)
    db.pharmacyherbaldrinks.insert_one(pharmacy_products)
    data={
        'pharm_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.pharmacy_herbaldrinksserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
@api_view(['GET'])   
def pharmacy_get_herbaldrinks(request,id):
    db = client['business']
    collection = db['pharmacyherbaldrinks']
 
    pharmacy_product = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True"})
    pharmacy_product_list = list(pharmacy_product)
    print(pharmacy_product_list)

    pharmacy_product_json = dumps(pharmacy_product_list)

    return JsonResponse(pharmacy_product_json, safe=False)

@api_view(['GET'])
def pharmacy_get_adminherbaldrinks(request):
    db = client['business']
    collection = db['pharmacyherbaldrinks']
    pharmacy_product = collection.find({})
    
    pharmacy_product_list = list(pharmacy_product)
  
    pharmacy_product_json = dumps(pharmacy_product_list)

    
    return JsonResponse(pharmacy_product_json, safe=False)
@api_view(['GET'])   
def pharmacy_get_my_herbaldrinks(request,id,product_id):
    db = client['business']
    collection = db['pharmacyherbaldrinks']
 
    pharmacy_products = collection.find({"pharm_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    pharmacy_products_list = list(pharmacy_products)
    print(pharmacy_products_list)
    pharmacy_products_json = dumps(pharmacy_products_list)

    return JsonResponse(pharmacy_products_json, safe=False)

    #delete
@api_view(['POST'])
def pharmacy_delete_herbaldrinks(request,id,product_id):
    db = client['business']
    collection = db['pharmacyherbaldrinks']

    #add
    collection.find_one({'pharm_id':id,'product_id':product_id})

    collection.delete_one({'pharm_id':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def pharmacy_update_herbaldrinks(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/pharmacy_herbaldrinks/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        pharmacy_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/pharmacy_herbaldrinks/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        pharmacy_products['other_images'] = other_imagelist

    except:
        pass
    pharmacy_products = dict(request.POST)

    db.pharmacyherbaldrinks.update_one({'pharm_id':id,'product_id':product_id} ,{'$set':pharmacy_products})

    return Response(id,status=status.HTTP_200_OK)

# pharmacy_herbaldrinksorder model
@api_view(["POST","GET"])
def herbaldrinksorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.pharmacy_ordermodel.objects.filter(Q(pharm_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['pharmacyherbaldrinks']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            herb_pro = dumps(alldata)
            
            return Response(herb_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 


#  d_original_dashboard
    
@api_view(['GET'])
def d_origin_total_revenue(request, id):
    if request.method == 'GET':
        total_revenue = models.dorigin_ordermodel.objects.filter(d_id=id).aggregate(total_revenue=Sum('total_amount'))['total_revenue'] or 0
        print(total_revenue)
        shop = models.d_originalmodel.objects.get(d_id=id)
        shop.total_revenue = total_revenue
        shop.save()
        return Response(data={'total_revenue': total_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def d_origin_mon_revenue(request, id):
    if request.method == 'GET':
        current_date = timezone.now().date()
        start_of_month = current_date.replace(day=1)
        end_of_month = start_of_month.replace(month=start_of_month.month + 1) - datetime.timedelta(days=1)
        monthly_revenue = models.dorigin_ordermodel.objects.filter(d_id=id, order_date__range=(start_of_month, end_of_month)).aggregate(monthly_revenue=Sum('total_amount'))['monthly_revenue']or 0
        d_origin = models.d_originalmodel.objects.get(d_id=id)
        d_origin.monthly_revenue = monthly_revenue
        d_origin.save()
        return Response(data={'monthly_revenue': monthly_revenue}, status=status.HTTP_200_OK)

@api_view(['GET'])
def d_origin_orderstatus(request,id):
    if request.method == 'GET':

        d_origin = models.dorigin_ordermodel.objects.filter(d_id=id).first()
        if not d_origin:
            return Response(data={'error': 'd_origin not found'}, status=status.HTTP_404_NOT_FOUND)
        delivered_count = models.dorigin_ordermodel.objects.filter(d_id=id, status='delivered').count()
        cancelled_count = models.dorigin_ordermodel.objects.filter(d_id=id, status='cancelled').count()
        on_process_count = models.dorigin_ordermodel.objects.filter(d_id=id, status='on_process').count()

        response_data = {
            'delivered_products': delivered_count,
            'cancelled_products': cancelled_count,
            'on_process_products': on_process_count
        }
        return Response(data=response_data, status=status.HTTP_200_OK)

@api_view(["POST"])
def d_originproduct_status_cancel(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.dorigin_ordermodel,order_id=id)
        print(pro)
        pro.status="cancelled"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def d_originproduct_status_on_process(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.dorigin_ordermodel,order_id=id)
        print(pro)
        if pro.status != "delivered" :
            pro.status="on_process"
            pro.save()

        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def d_originproduct_status_delivered(request,id):
    try:
        print(request.POST)
        pro=get_object_or_404(models.dorigin_ordermodel,order_id=id)
        print(pro)
        pro.status="delivered"
        pro.save()
        return Response("success",status=status.HTTP_200_OK)
    except:
        return Response("nostatus",status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def d_origin_all_products(request,id):
    if request.method== "GET":
        d_origin_data = models.d_originalproductsmodel.objects.filter(d_id=id)
        all_data = [
            d_origin_data
        ]
        # Calculate the total count
        total_count = sum(data.count() for data in all_data)
        print(total_count)
        return Response(data={'total_count': total_count}, status=status.HTTP_200_OK)
# d_original
@api_view(['POST'])
def d_original(request,id):
    # print(request.data)
    # print(request.FILES)
    fs = FileSystemStorage()
    aadhar = str(request.FILES['aadhar']).replace(" ", "_")
    aadhar_path = fs.save(f"api/d_original/{id}/aahar/"+aadhar, request.FILES['aadhar'])
    pan_file = str(request.FILES['pan_file']).replace(" ", "_")
    pan_file_path = fs.save(f"api/d_original/{id}/pan_file/"+pan_file, request.FILES['pan_file'])
    profile = str(request.FILES['profile']).replace(" ", "_")
    profile_path = fs.save(f"api/d_original/{id}/profile/"+profile, request.FILES['profile'])
    bank_passbook = str(request.FILES['bank_passbook']).replace(" ", "_")
    bank_passbook_path = fs.save(f"api/d_original/{id}/bank_passbook/"+bank_passbook, request.FILES['bank_passbook'])
    gst_file = str(request.FILES['gst_file']).replace(" ", "_")
    gst_file_path = fs.save(f"api/d_original/{id}/gst_file/"+gst_file, request.FILES['gst_file'])

    aadhar_paths = all_image_url+fs.url(aadhar_path)
    pan_file_paths = all_image_url+fs.url(pan_file_path)
    profile_paths = all_image_url+fs.url(profile_path)
    bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    gst_file_paths = all_image_url+fs.url(gst_file_path)
    x = datetime.datetime.now()
    ds_id=business_extension.d_id_generate()
    while True:
        if id == ds_id:
            ds_id=business_extension.d_id_generate()
        else:
            break

    data = {
        'Business_id': id,
        'd_id':ds_id,
        'seller_name': request.POST['seller_name'],
        'business_name': request.POST['business_name'],
        'pan_number': request.POST['pan_number'],
        'gst': request.POST['gst'],
        'contact': request.POST['contact'],
        'alternate_contact': request.POST['alternate_contact'],
        'pin_number': request.POST['pin_number'],
        'aadhar_number' : request.POST['aadhar_number'],
        'door_number' : request.POST['door_number'],
        'street_name' : request.POST['street_name'],
        'area' : request.POST['area'],        
        'fssa':request.POST['fssa'],
        'region':request.POST['region'],
        'pin_your_location': request.POST['pin_your_location'],           
        'name': request.POST['name'],           
        'account_number':request.POST['account_number'],
        'ifsc_code':request.POST['ifsc_code'],
        'upi_id':request.POST['upi_id'],
        'gpay_number':request.POST['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
        }

    print(data)
    basicdetailsserializer = business_serializers.d_original_serializer(data=data)
    
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def d_original_alldata(request):
    if request.method == "GET":
        data = d_originalmodel.objects.all()
        serializer = business_serializers.d_original_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def my_d_original_data(request,id):
    if request.method == "GET":
        data = d_originalmodel.objects.get(d_id=id)
        print(data)
        serializer = business_serializers.d_original_list_serializer(data,many=False)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
def business_d_original_data(request,id):
    if request.method == "GET":
        data = d_originalmodel.objects.filter(Business_id=id)
        serializer = business_serializers.d_original_list_serializer(data,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def d_original_update(request,id,d_id):
    fs=FileSystemStorage

    d_original_data = d_originalmodel.objects.get(Business_id=id,d_id=d_id)
    print(d_original_data)
    d_original_datas = d_originalmodel.objects.filter(Business_id=id,d_id=d_id).values()[0]

   
    if "aadhar" in request.FILES:
        aadhar = str(request.FILES['aadhar']).replace(" ","_")
        aadhar_path = fs.save(f"api/d_original/{id}/aadhar/"+aadhar, request.FILES["aadhar"])
        aadhar_paths = all_image_url+fs.url(aadhar_path)
    else:
        aadhar_paths = d_original_datas["aadhar"]
        print(aadhar_paths)
    if "pan_file" in request.FILES:
        pan_file = str(request.FILES["pan_file"]).replace(" ","_")
        pan_file_path = fs.save(f"api/d_original/{id}/pan_file/"+pan_file, request.FILES["pan_file"])

        pan_file_paths = all_image_url+fs.url(pan_file_path)
    else:
        pan_file_paths = d_original_datas["pan_file"]
    if "profile" in request.FILES:
        profile = str(request.FILES["profile"]).replace(" ","_")
        profile_path = fs.save(f"api/d_original/{id}/profile/"+profile, request.FILES["profile"])
        profile_paths = all_image_url+fs.url(profile_path)
    else:
        profile_paths = d_original_datas["profile"]
    if "bank_passbook" in request.FILES:
        bank_passbook = str(request.FILES["bank_passbook"]).replace(" ","_")
        bank_passbook_path = fs.save(f"api/d_original/{id}/bank_passbook/"+bank_passbook, request.FILES["bank_passbook"])
        bank_passbook_paths = all_image_url+fs.url(bank_passbook_path)
    else:
        bank_passbook_paths = d_original_datas["bank_passbook"]
    if "gst_file" in request.FILES:
        gst_file = str(request.FILES["gst_file"]).replace(" ","_")
        gst_file_path = fs.save(f"api/d_original/{id}/gst_file/"+gst_file, request.FILES["gst_file"])
        gst_file_paths = all_image_url+fs.url(gst_file_path)
    else:
        gst_file_paths = d_original_datas["gst_file"]
    
    data = {
        'seller_name': request.data['seller_name'],
        'business_name': request.data['business_name'],
        'pan_number': request.data['pan_number'],
        'gst': request.data['gst'],
        'contact': request.data['contact'],
        'alternate_contact': request.data['alternate_contact'],
        'pin_number': request.data['pin_number'],
        'aadhar_number' : request.data['aadhar_number'],
        'door_number' : request.data['door_number'],
        'street_name' : request.data['street_name'],
        'area' : request.data['area'],
        'fssa':request.data['fssa'],
        'region':request.data['region'],
        'pin_your_location': request.data['pin_your_location'],           
        'name': request.data['name'],           
        'account_number':request.data['account_number'],
        'ifsc_code':request.data['ifsc_code'],
        'upi_id':request.data['upi_id'],
        'gpay_number':request.data['gpay_number'],
        'aadhar':aadhar_paths,
        'pan_file': pan_file_paths,
        'profile': profile_paths,
        'bank_passbook': bank_passbook_paths,
        'gst_file': gst_file_paths,
        'date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)

    }
    print(data)
    dataserializer = business_serializers.d_original_edit_serializer(instance=d_original_data, data=data, partial=True)
    print(dataserializer)
    if dataserializer.is_valid():
      
        dataserializer.save()
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)


# d_original product
@api_view(['POST'])
def d_original_product(request,id):
    product_id = business_extension.product_id_generate()
    while True:
        if id == product_id:
            product_id = business_extension.product_id_generate()
        else:
            break
    db = client['business']
    #add
    fs = FileSystemStorage()

    primary_image = str(request.FILES['primary_image']).replace(" ", "_")
    primary_image_path = fs.save(f"api/d_original_product/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
    primary_image_paths = all_image_url+fs.url(primary_image_path)
    print(primary_image_paths)
    other_image = []
    other_imagelist = []
    for sav in request.FILES.getlist('other_images'):
        ot = fs.save(f"api/d_original_product/{id}/other_images/"+sav.name, sav)
        other_image.append(str(ot).replace(" ","_"))
            
        print(other_image)
        for iname in other_image:
            other_images_path = iname
            other_imagelist.append(all_image_url+fs.url(other_images_path))
    commission =10
    gst = 3
    actualprice=request.POST["actual_price"]
    discountprice=request.POST["discount_price"]
    sellingprice = int(actualprice) - int(discountprice)
    commision = sellingprice + ((commission/100) * sellingprice)

    selling_price = commision + ((gst/100) * commision)
    d_original_products = dict(request.POST)
    d_original_products['d_id'] = id
    d_original_products['product_id'] = product_id
    d_original_products['primary_image'] = primary_image_paths
    d_original_products['other_images'] = other_imagelist
    d_original_products['selling_price'] = selling_price

    print(d_original_products)
    db.d_originalproduct.insert_one(d_original_products)
    data={
        'd_id' : id,
        'product_id' : product_id
    }
    print(data)

    basicdetailsserializer = business_serializers.d_originalproductsserializer(data=data)
    
    if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
    else:
        print("serializer prblm")
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    
    
    
@api_view(['GET'])
def d_original_get_adminproduct(request):
    db = client['business']
    collection = db['d_originalproduct']
    d_original_product = collection.find({})
    
    d_original_product_list = list(d_original_product)
  
    d_original_product_json = dumps(d_original_product_list)

    return JsonResponse(d_original_product_json, safe=False)
@api_view(['GET'])   
def d_original_get_product(request,id):
    db = client['business']
    collection = db['d_originalproduct']
 
    d_original_product = collection.find({"d_id": {"$regex":f"^{id}"},"status":"True"})
    d_original_product_list = list(d_original_product)
    print(d_original_product_list)

    d_original_product_json = dumps(d_original_product_list)

    return JsonResponse(d_original_product_json, safe=False)

@api_view(['GET'])   
def d_original_get_my_product(request,id,product_id):
    db = client['business']
    collection = db['d_originalproduct']
 
    d_original_products = collection.find({"d_id": {"$regex":f"^{id}"},"status":"True","product_id":product_id})
    d_original_products_list = list(d_original_products)
    print(d_original_products_list)
    d_original_products_json = dumps(d_original_products_list)

    return JsonResponse(d_original_products_json, safe=False)
    #delete
@api_view(['POST'])
def d_original_delete_product(request,id,product_id):
    db = client['business']
    collection = db['d_originalproduct']

    #add

    collection.find_one({'d_id ':id,'product_id':product_id})

    collection.delete_one({'d_id ':id,'product_id':product_id})
    return Response(id,status=status.HTTP_200_OK)
@api_view(['POST'])
def d_original_update_product(request,id,product_id):
    db = client['business']
    fs = FileSystemStorage()
    try:
        primary_image = str(request.FILES['primary_image']).replace(" ", "_")
        primary_image_path = fs.save(f"api/d_original_product/{id}/primary_image/"+primary_image, request.FILES['primary_image'])
        primary_image_paths = all_image_url+fs.url(primary_image_path)
        print(primary_image_paths)
        d_original_products['primary_image'] = primary_image_paths

    except:
        pass
    try:
        other_image = []
        other_imagelist = []
        for sav in request.FILES.getlist('other_images'):
            ot = fs.save(f"api/d_original_product/{id}/other_images/"+sav.name, sav)
            other_image.append(str(ot).replace(" ","_"))
                
            print(other_image)
            for iname in other_image:
                other_images_path = iname
                other_imagelist.append(all_image_url+fs.url(other_images_path))
        d_original_products['other_images'] = other_imagelist

    except:
        pass
    d_original_products = dict(request.POST)

    db.d_originalproduct.update_one({'d_id':id,'product_id':product_id} ,{'$set':d_original_products})

    return Response(id,status=status.HTTP_200_OK)


#d_originalproductorder model
@api_view(["POST","GET"])
def productorder_date(request,id):
    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        data=models.dorigin_ordermodel.objects.filter(Q(d_id=id) & Q(status="delivered")& Q(delivery_date__range=[from_date, to_date])).values()
        print(data,"data")
        pro_data=[]
        for item in data:
            pro_id = item.get("product_id")
            pro_data.append(pro_id)
            
        if pro_data:
            # Query MongoDB collection
            db = client['business']
            collection = db['d_originalproduct']
            alldata = []
            for product_info in pro_data:
                proget = collection.find_one({"product_id": product_info})
                alldata.append(proget)
                print(proget)
            print(type(alldata))
            do_pro = dumps(alldata)
            
            return Response(do_pro, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST) 



@api_view(["GET"])
def shopproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.shop_ordermodel.objects.filter(shop_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # electrical Collection
        collection_electro = db['shopelectronics']
        alldata_elect = []
        for product_info in pro_data:
            proget = collection_electro.find_one({"product_id": product_info})
            alldata_elect.append(proget)
            print(proget)
    # Mobile Collection
        collection_mobile = db['shopmobile']
        alldata_mobile = []
        for product_info in pro_data:
            proget_mobile = collection_mobile.find_one({"product_id": product_info})
            if proget_mobile:
                alldata_mobile.append(proget_mobile)
                print(proget_mobile)

    # furniture Collection
        collection_fur = db['shopfurniture']
        alldata_fur = []
        for product_info in pro_data:
            proget_fur = collection_fur.find_one({"product_id": product_info})
            if proget_fur:
                alldata_fur.append(proget_fur)
                print(proget_fur)

    # shopsports collection
        collection_sport = db['shopsports']
        alldata_sport = []
        for product_info in pro_data:
            proget_sport = collection_sport.find_one({"product_id": product_info})
            if proget_sport:
                alldata_sport.append(proget_sport)
                print(proget_sport)  
        
    # shoptoys collection
        collection_toys = db['shoptoys']
        alldata_toys = []
        for product_info in pro_data:
            proget_toys = collection_toys.find_one({"product_id": product_info})
            if proget_toys:
                alldata_toys.append(proget_toys)
                print(proget_toys)

    # shopfashion collection
        collection_fashion = db['shopfashion']
        alldata_fashion = []
        for product_info in pro_data:
            proget_fashion = collection_fashion.find_one({"product_id": product_info})
            if proget_fashion:
                alldata_fashion.append(proget_fashion)
                print(proget_fashion) 
    # shopkitchen collection
        collection_kitchen = db['shopkitchen']
        alldata_kitchen = []
        for product_info in pro_data:
            proget_kitchen = collection_kitchen.find_one({"product_id": product_info})
            if proget_kitchen:
                alldata_kitchen.append(proget_kitchen)
                print(proget_kitchen)  
        

    # shopgroceries collection
        collection_groceries = db['shopgroceries']
        alldata_groceries = []
        for product_info in pro_data:
            proget_groceries = collection_groceries.find_one({"product_id": product_info})
            if proget_groceries:
                alldata_groceries.append(proget_groceries)
                print(proget_groceries)  
    # shoppersonalcare collection
        collection_personalcare = db['shoppersonalcare']
        alldata_personalcare = []
        for product_info in pro_data:
            proget_personalcare = collection_personalcare.find_one({"product_id": product_info})
            if proget_personalcare:
                alldata_personalcare.append(proget_personalcare)
                print(proget_personalcare)  

    # shopbooks collection
        collection_books = db['shopbooks']
        alldata_books = []
        for product_info in pro_data:
            proget_books = collection_books.find_one({"product_id": product_info})
            if proget_books:
                alldata_books.append(proget_books)
                print(proget_books)  

    # shophealthcare collection
        collection_healthcare = db['shophealthcare']
        alldata_healthcare = []
        for product_info in pro_data:
            proget_healthcare = collection_healthcare.find_one({"product_id": product_info})
            if proget_healthcare:
                alldata_healthcare.append(proget_healthcare)
                print(proget_healthcare)  


    # shopautoaccessories collection
        collection_autoaccessories = db['shopautoaccessories']
        alldata_autoaccessories = []
        for product_info in pro_data:
            proget_autoaccessories = collection_autoaccessories.find_one({"product_id": product_info})
            if proget_autoaccessories:
                alldata_autoaccessories.append(proget_autoaccessories)
                print(proget_autoaccessories)  

    # shopappliances collection  
        collection_appliances = db['shopappliances']
        alldata_appliances = []
        for product_info in pro_data:
            proget_appliances = collection_appliances.find_one({"product_id": product_info})
            if proget_appliances:
                alldata_appliances.append(proget_appliances)
                print(proget_appliances)  
    
    # shoppetsupplies collection  
        collection_petsupplies = db['shoppetsupplies']
        alldata_petsupplies = []
        for product_info in pro_data:
            proget_petsupplies = collection_petsupplies.find_one({"product_id": product_info})
            if proget_petsupplies:
                alldata_petsupplies.append(proget_petsupplies)
                print(proget_petsupplies)  


        # print(type(alldata_elect))
        # print(type(alldata_mobile))
        # print(type(alldata_fur))
        # print(type(alldata_sport))
        # print(type(alldata_toys))
        # print(type(alldata_kitchen))
        # print(type(alldata_autoaccessories))
        # print(type(alldata_healthcare))
        # print(type(alldata_books))
        # print(type(alldata_personalcare))
        # print(type(alldata_groceries))
        # print(type(alldata_appliances))
        # print(type(alldata_petsupplies))
        # print(type(alldata_fashion))

        shop_elect = dumps(alldata_elect)
        shop_mobile = dumps(alldata_mobile)
        shop_fur = dumps(alldata_fur)
        shop_sport = dumps(alldata_sport)
        shop_toys = dumps(alldata_toys)
        shop_healthcare = dumps(alldata_healthcare)
        shop_books = dumps(alldata_books)
        shop_personalcare = dumps(alldata_personalcare)
        shop_kitchen = dumps(alldata_kitchen)
        shop_groceries = dumps(alldata_groceries)
        shop_autoaccessories = dumps(alldata_autoaccessories)
        shop_appliances = dumps(alldata_appliances)
        shop_petsupplies = dumps(alldata_petsupplies)
        shop_fashion = dumps(alldata_fashion)
       
     
        return JsonResponse({"mobile_products": shop_mobile, "electro_products":shop_elect, "furniture_products":shop_fur,"sport_products":shop_sport, "toys_products":shop_toys, "health_products":shop_healthcare,"book_products":shop_books,"personalcare":shop_personalcare,"kitchen":shop_kitchen,"groceries":shop_groceries, "autoaccessories":shop_autoaccessories,"appliances":shop_appliances,"petsupplies":shop_petsupplies,"fashion":shop_fashion}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)





# jwellery products history
@api_view(["GET"])
def jewelproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.jewel_ordermodel.objects.filter(jewel_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # jewellerygold Collection
        collection_gold = db['jewelgold']
        alldata_gold = []
        for product_info in pro_data:
            proget = collection_gold.find_one({"product_id": product_info})
            alldata_gold.append(proget)
            print(proget)

    # jewellerysilver Collection
        collection_silver = db['jewelsilver']
        alldata_silver = []
        for product_info in pro_data:
            proget = collection_silver.find_one({"product_id": product_info})
            alldata_silver.append(proget)
            print(proget)

        
    
        print(type(alldata_gold))
        print(type(alldata_silver))
     
        jewel_gold = dumps(alldata_gold)
        jewel_silver = dumps(alldata_silver)

       
     
        return JsonResponse({"gold_products":jewel_gold , "silver_products":jewel_silver}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)




# food products history
@api_view(["GET"])
def foodproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.food_ordermodel.objects.filter(food_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # foodtiffen Collection
        collection_tiffen = db['foodtiffen']
        alldata_tiffen = []
        for product_info in pro_data:
            proget = collection_tiffen.find_one({"product_id": product_info})
            alldata_tiffen.append(proget)
            print(proget)
        print(type(alldata_tiffen))
        food_tiffen = dumps(alldata_tiffen)


    # foodmeals Collection
        collection_meals = db['foodmeals']
        alldata_meals = []
        for product_info in pro_data:
            proget = collection_meals.find_one({"product_id": product_info})
            alldata_meals.append(proget)
            print(proget)
       
        food_meals = dumps(alldata_meals)
    # foodbiriyani Collection
        collection_biriyani = db['foodbiriyani']
        alldata_biriyani = []
        for product_info in pro_data:
            proget = collection_biriyani.find_one({"product_id": product_info})
            alldata_biriyani.append(proget)
            print(proget)
       
        food_biriyani = dumps(alldata_biriyani)


    # foodchickenbiriyani Collection
        collection_chickenbiriyani = db['foodchickenbiriyani']
        alldata_chickenbiriyani = []
        for product_info in pro_data:
            proget = collection_chickenbiriyani.find_one({"product_id": product_info})
            alldata_chickenbiriyani.append(proget)
            print(proget)
       
        food_chickenbiriyani = dumps(alldata_chickenbiriyani)
    # foodbeef Collection
        collection_beef = db['foodbeef']
        alldata_beef = []
        for product_info in pro_data:
            proget = collection_beef.find_one({"product_id": product_info})
            alldata_beef.append(proget)
            print(proget)
       
        food_beef = dumps(alldata_beef)

    # foodchinese Collection
        collection_chinese = db['foodchinese']
        alldata_chinese = []
        for product_info in pro_data:
            proget = collection_chinese.find_one({"product_id": product_info})
            alldata_chinese.append(proget)
            print(proget)
       
        food_chinese = dumps(alldata_chinese)

    # foodpizza Collection
        collection_pizza = db['foodpizza']
        alldata_pizza = []
        for product_info in pro_data:
            proget = collection_pizza.find_one({"product_id": product_info})
            alldata_pizza.append(proget)
            print(proget)
       
        food_pizza = dumps(alldata_pizza)


    # foodteacoffe Collection
        collection_teacoffe = db['foodteacoffe']
        alldata_teacoffe = []
        for product_info in pro_data:
            proget = collection_teacoffe.find_one({"product_id": product_info})
            alldata_teacoffe.append(proget)
            print(proget)
       
        food_teacoffe = dumps(alldata_teacoffe)

    # foodicecream Collection
        collection_icecream = db['foodicecream']
        alldata_icecream = []
        for product_info in pro_data:
            proget = collection_icecream.find_one({"product_id": product_info})
            alldata_icecream.append(proget)
            print(proget)
       
        food_icecream = dumps(alldata_icecream)

    # foodfiredchicken Collection
        collection_firedchicken = db['foodfiredchicken']
        alldata_firedchicken = []
        for product_info in pro_data:
            proget = collection_firedchicken.find_one({"product_id": product_info})
            alldata_firedchicken.append(proget)
            print(proget)
       
        food_firedchicken = dumps(alldata_firedchicken)

    # foodburger Collection
        collection_burger = db['foodburger']
        alldata_burger = []
        for product_info in pro_data:
            proget = collection_burger.find_one({"product_id": product_info})
            alldata_burger.append(proget)
            print(proget)
       
        food_burger = dumps(alldata_burger)
    # foodcake Collection
        collection_cake = db['foodcake']
        alldata_cake = []
        for product_info in pro_data:
            proget = collection_cake.find_one({"product_id": product_info})
            alldata_cake.append(proget)
            print(proget)
       
        food_cake = dumps(alldata_cake)
    # foodbakery Collection
        collection_bakery = db['foodbakery']
        alldata_bakery = []
        for product_info in pro_data:
            proget = collection_bakery.find_one({"product_id": product_info})
            alldata_bakery.append(proget)
            print(proget)
       
        food_bakery = dumps(alldata_bakery)
     
        return JsonResponse({"tiffen_products":food_tiffen , "meals_products":food_meals,"biriyani":food_biriyani, "chickenbiriyani":food_chickenbiriyani,"beef":food_beef,"chinese":food_chinese,"chinese":food_chinese,"pizza":food_pizza,"teacoffe":food_teacoffe,"icecream":food_icecream,"firedchicken":food_firedchicken,"burger":food_burger,"cake":food_cake,"bakery":food_bakery}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)



# freshcutsroducts history
@api_view(["GET"])
def freshproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.fresh_ordermodel.objects.filter(fresh_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # freshchicken Collection
        collection_chicken = db['freshchicken']
        alldata_chicken = []
        for product_info in pro_data:
            proget = collection_chicken.find_one({"product_id": product_info})
            alldata_chicken.append(proget)
            print(proget)

        fresh_chicken = dumps(alldata_chicken)

    # freshmutton Collection
        collection_mutton = db['freshmutton']
        alldata_mutton = []
        for product_info in pro_data:
            proget = collection_mutton.find_one({"product_id": product_info})
            alldata_mutton.append(proget)
            print(proget)

        fresh_mutton = dumps(alldata_mutton)
    # freshbeef Collection
        collection_beef = db['freshbeef']
        alldata_beef = []
        for product_info in pro_data:
            proget = collection_beef.find_one({"product_id": product_info})
            alldata_beef.append(proget)
            print(proget)

        fresh_beef = dumps(alldata_beef)
    # freshfishseafood Collection
        collection_fishseafood = db['freshfishseafood']
        alldata_fishseafood = []
        for product_info in pro_data:
            proget = collection_fishseafood.find_one({"product_id": product_info})
            alldata_fishseafood.append(proget)
            print(proget)

        fresh_fishseafood = dumps(alldata_fishseafood)
    
    # freshdryfish Collection
        collection_dryfish = db['freshdryfish']
        alldata_dryfish = []
        for product_info in pro_data:
            proget = collection_dryfish.find_one({"product_id": product_info})
            alldata_dryfish.append(proget)
            print(proget)

        fresh_dryfish = dumps(alldata_dryfish)
    # freshprawns Collection
        collection_prawns = db['freshprawns']
        alldata_prawns = []
        for product_info in pro_data:
            proget = collection_prawns.find_one({"product_id": product_info})
            alldata_prawns.append(proget)
            print(proget)

        fresh_prawns = dumps(alldata_prawns)
    # freshegg Collection
        collection_egg = db['freshegg']
        alldata_egg = []
        for product_info in pro_data:
            proget = collection_egg.find_one({"product_id": product_info})
            alldata_egg.append(proget)
            print(proget)

        fresh_egg = dumps(alldata_egg)

    # freshpond Collection
        collection_pond = db['freshpond']
        alldata_pond = []
        for product_info in pro_data:
            proget = collection_pond.find_one({"product_id": product_info})
            alldata_pond.append(proget)
            print(proget)

        fresh_pond = dumps(alldata_pond)
    # freshmeatmasala Collection
        collection_meatmasala = db['freshmeatmasala']
        alldata_meatmasala = []
        for product_info in pro_data:
            proget = collection_meatmasala.find_one({"product_id": product_info})
            alldata_meatmasala.append(proget)
            print(proget)

        fresh_meatmasala = dumps(alldata_meatmasala)
    # freshcombo Collection
        collection_combo = db['freshcombo']
        alldata_combo = []
        for product_info in pro_data:
            proget = collection_combo.find_one({"product_id": product_info})
            alldata_combo.append(proget)
            print(proget)

        fresh_combo = dumps(alldata_combo)
    # freshchoppedveg Collection
        collection_choppedveg = db['freshchoppedveg']
        alldata_choppedveg = []
        for product_info in pro_data:
            proget = collection_choppedveg.find_one({"product_id": product_info})
            alldata_choppedveg.append(proget)
            print(proget)

        fresh_choppedveg = dumps(alldata_choppedveg)
        return JsonResponse({"chicken_products":fresh_chicken , "choppedveg":fresh_choppedveg,"combo":fresh_combo,"meatmasala":fresh_meatmasala,"pond":fresh_pond,"mutton":fresh_mutton,"egg":fresh_egg,"prawns":fresh_prawns,"dryfish":fresh_dryfish,"fishseafood":fresh_fishseafood,"beef":fresh_beef}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    

#  dmioproducts history
@api_view(["GET"])
def dmioproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.daily_ordermodel.objects.filter(dmio_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # dmiogrocery Collection
        collection_grocery = db['dmiogrocery']
        alldata_grocery = []
        for product_info in pro_data:
            proget = collection_grocery.find_one({"product_id": product_info})
            alldata_grocery.append(proget)
            print(proget)
        dmio_grocery = dumps(alldata_grocery)
    # dmiomeat Collection
        collection_meat = db['dmiomeat']
        alldata_meat = []
        for product_info in pro_data:
            proget = collection_meat.find_one({"product_id": product_info})
            alldata_meat.append(proget)
            print(proget)

        print(type(alldata_meat))
        dmio_meat = dumps(alldata_meat)
      
    # dmiofish Collection
        collection_fish = db['dmiofish']
        alldata_fish = []
        for product_info in pro_data:
            proget = collection_fish.find_one({"product_id": product_info})
            alldata_fish.append(proget)
            print(proget)

        print(type(alldata_fish))
        dmio_fish = dumps(alldata_fish)

    # dmioeggs Collection
        collection_eggs = db['dmioeggs']
        alldata_eggs = []
        for product_info in pro_data:
            proget = collection_eggs.find_one({"product_id": product_info})
            alldata_eggs.append(proget)
            print(proget)

        print(type(alldata_eggs))
        dmio_eggs = dumps(alldata_eggs)
    
    # dmiofruits Collection
        collection_fruits = db['dmiofruits']
        alldata_fruits = []
        for product_info in pro_data:
            proget = collection_fruits.find_one({"product_id": product_info})
            alldata_fruits.append(proget)
            print(proget)

        print(type(alldata_fruits))
        dmio_fruits = dumps(alldata_fruits)
     
    # dmiovegitables Collection
        collection_vegitables = db['dmiovegitables']
        alldata_vegitables = []
        for product_info in pro_data:
            proget = collection_vegitables.find_one({"product_id": product_info})
            alldata_vegitables.append(proget)
            print(proget)

        print(type(alldata_vegitables))
        dmio_vegitables = dumps(alldata_vegitables)
    # dmiodairy Collection
        collection_dairy = db['dmiodairy']
        alldata_dairy = []
        for product_info in pro_data:
            proget = collection_dairy.find_one({"product_id": product_info})
            alldata_dairy.append(proget)
            print(proget)

        print(type(alldata_dairy))
        dmio_dairy = dumps(alldata_dairy)
       
     
        return JsonResponse({"grocery":dmio_grocery , "meat":dmio_meat,"fish":dmio_fish,"eggs":dmio_eggs,"fruits":dmio_fruits,"vegitables":dmio_vegitables,"dairy":dmio_dairy}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)



#  pharmacyproducts history
@api_view(["GET"])
def pharmacyproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.pharmacy_ordermodel.objects.filter(pharm_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # pharmallopthy Collection
        collection_allo = db['pharmacyallopathic']
        alldata_allo = []
        for product_info in pro_data:
            proget = collection_allo.find_one({"product_id": product_info})
            alldata_allo.append(proget)
            print(proget)

        pharm_allo = dumps(alldata_allo)
    # pharmayurvedic Collection
        collection_ayur = db['pharmacyayurvedic']
        alldata_ayur = []
        for product_info in pro_data:
            proget = collection_ayur.find_one({"product_id": product_info})
            alldata_ayur.append(proget)
            print(proget)

        pharm_ayur = dumps(alldata_ayur)    
    # pharmaysiddha Collection
        collection_siddha = db['pharmacysiddha']
        alldata_siddha = []
        for product_info in pro_data:
            proget = collection_siddha.find_one({"product_id": product_info})
            alldata_siddha.append(proget)
            print(proget)

        pharm_siddha = dumps(alldata_siddha)
    # pharmayunani Collection
        collection_unani = db['pharmacyunani']
        alldata_unani = []
        for product_info in pro_data:
            proget = collection_unani.find_one({"product_id": product_info})
            alldata_unani.append(proget)
            print(proget)

        pharm_unani = dumps(alldata_unani)

    # pharmayherbal Collection
        collection_herbal = db['pharmacyherbaldrinks']
        alldata_herbal = []
        for product_info in pro_data:
            proget = collection_herbal.find_one({"product_id": product_info})
            alldata_herbal.append(proget)
            print(proget)

        pharm_herbal = dumps(alldata_herbal)

     
        return JsonResponse({"allo_products":pharm_allo , "ayur_products":pharm_ayur,"siddha":pharm_siddha,"unani":pharm_unani,"herbal_products":pharm_herbal}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)




# d_original products history
@api_view(["GET"])
def d_originalproducts_orderhistory(request, id):
    if request.method == "GET":
        data = models.dorigin_ordermodel.objects.filter(d_id=id, payment_status=True)  
        print(data)
      
        pro_data = []
        for order in data:
            print(order)
            pro_id = order.product_id
            pro_data.append(pro_id)
        print(pro_data)
    # mongodb collections
        db = client['business']
    # d_originpro Collection
        collection_d_originpro = db['d_originalproduct']
        alldata_d_originpro = []
        for product_info in pro_data:
            proget = collection_d_originpro.find_one({"product_id": product_info})
            alldata_d_originpro.append(proget)
            print(proget)
       
     
        d_origin_pro = dumps(alldata_d_originpro)
     
        return JsonResponse({"d_origin_pro":d_origin_pro}, status=status.HTTP_200_OK)  
    else:
        return JsonResponse({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)