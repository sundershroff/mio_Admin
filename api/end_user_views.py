from django.shortcuts import render,get_object_or_404
from api import business_serializers,end_user_serializers
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import end_user_extension
from rest_framework.decorators import api_view
from api import models
import json
import datetime
from bson.json_util import dumps,loads
from pymongo import MongoClient
import math

client = MongoClient('localhost', 27017)
all_image_url = "http://127.0.0.1:3000/"
x = datetime.datetime.now()

@api_view(['POST'])
def end_user_signup(request):
    try:
        try:
            if end_user_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'uid': end_user_extension.id_generate(),
                    'otp': end_user_extension.otp_generate(),
                    'full_name':request.data["full_name"],
                    'email': request.data["email"],
                    'phone_number': request.data['phone_number'],
                    'password': request.data["password"],
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = end_user_serializers.SignupSerializer(data=datas)
                print(dataserializer)
                
                if dataserializer.is_valid():            
                    dataserializer.save()
                    print("Valid Data")
                    end_user_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def end_user_otp(request, id):
    try:
        try:
            if end_user_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userData = models.End_Usermodel.objects.get(uid=id)
                    print(userData)
                    serializer_validate = end_user_serializers.OTPSerializer(
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
def end_user_signin(request):
    try:
       
        try:
            if end_user_extension.validate_email(request.data['email']):
                if end_user_extension.verify_user(request.data['email'], request.data['password']):
                    if end_user_extension.verify_user_otp(request.data['email']):
                        if end_user_extension.get_user_id(request.data['email']):
                            return Response(end_user_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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


@api_view(["GET"])
def all_users_data(request):
    if request.method == "GET":
        data=models.End_Usermodel.objects.all()
        serializers=end_user_serializers.EnduserSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def endresend_otp(request,id):

    try:
        try:
            new_otp = end_user_extension.otp_generate()
            user = models.End_Usermodel.objects.get(uid=id)
            email = user.email 
            print(f"Email: {email}")
            end_user_extension.send_mail(email, new_otp)
            user.otp = new_otp
            user.save()
            return Response({"New OTP": new_otp, "Email": email}, status=status.HTTP_200_OK)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def endforget_password(request):

    try:
        try:
            print(request.POST)
            if end_user_extension.validate_email(request.data['email']):
                Data = models.End_Usermodel.objects.get(email=request.data['email'])

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
def end_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = models.End_Usermodel.objects.get(uid=id)
        
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
     
        path = fs.save(f"api/end_user/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path           
        }

        print(data)
        basicdetailsserializer = end_user_serializers.profile_picture_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def end_user_address(request,id):
    try:
        if request.method == "POST":
            print(request.POST)
            userdata = models.End_Usermodel.objects.get(uid=id)
            data={
                'doorno' : request.data["doorno"],
                'area' : request.data["area"],
                'landmark': request.data["landmark"],
                'place' : request.data["place"],
                'district' : request.data["district"],
                'state' : request.data["state"],
                'pincode' : request.data["pincode"],
                
               }
            
            # userdata.address_data = data
            # userdata.save()
            addressSerializer = end_user_serializers.AddressSerializer(instance=userdata, data=data, partial=True)
            if addressSerializer.is_valid():
                addressSerializer.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def end_user_tempaddress(request,id):
    try:
        if request.method == "POST":
            print(request.POST)
            userdata = models.End_Usermodel.objects.get(uid=id)
            data={
                'doorno' : request.data["doorno"],
                'area' : request.data["area"],
                'landmark': request.data["landmark"],
                'place' : request.data["place"],
                'district' : request.data["district"],
                'state' : request.data["state"],
                'pincode' : request.data["pincode"],
               }
            
            # userdata.address_data = data
            # userdata.save()
            addressSerializer = end_user_serializers.TempAddressSerializer(instance=userdata, data=data, partial=True)
            if addressSerializer.is_valid():
                addressSerializer.save()
                print("Valid Data")
                return Response(id, status=status.HTTP_200_OK)
            else:
                return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def enduser_profile_update(request,id):
    
    print(request.FILES)
    fs = FileSystemStorage()
    userdata = models.End_Usermodel.objects.get(uid=id)
    print(userdata)
    datas = models.End_Usermodel.objects.filter(uid=id).values()[0]
    print(datas)
    
    if "profile_picture" in request.FILES:
        profile_picture= str(request.FILES['profile_picture']).replace(" ", "_")
        path = fs.save(f"api/business/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)
    else:
        full_path = datas['profile_picture']
    print("valid")

    data = {
        'profile_picture': full_path
        
    }

    # print(data)
    basicdetailsserializer = end_user_serializers.update_acc_serializer(
        instance=userdata, data=data, partial=True)
    if basicdetailsserializer.is_valid():
        basicdetailsserializer.save()
        print("Valid Data")
        return Response(id, status=status.HTTP_200_OK)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["GET"])
def single_users_data(request,id):
    if request.method == "GET":
        data=models.End_Usermodel.objects.filter(uid=id)
        print(data)
        serializers=end_user_serializers.EnduserSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

# ....................shop products............
#   ......before login--------
@api_view(['GET'])
def all_shopproducts(request): 
    if request.method == "GET":
        data= models.shop_productsmodel.objects.filter(status=True)
        print(data)
        alldataserializer= business_serializers.shop_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_shop(request,subcategory):
    if request.method == "GET":
        data = models.shop_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_single_shopproduct(request,id,product_id):
    if request.method == "GET":
        # user_id= models.End_Usermodel.objects.get(uid=user_id)
        # print(user_id)
        data = models.shop_productsmodel.objects.filter(shop_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login...............
@api_view(['GET'])
def user_get_all_shopproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.shop_productsmodel.objects.filter(shop_id=id,status=True)
        alldataserializer= business_serializers.shop_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_shop(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.shop_productsmodel.objects.filter(shop_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_shopproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.shop_productsmodel.objects.filter(shop_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.shop_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# ................jewellery products.............

@api_view(['GET'])
def all_jewelproducts(request):
    if request.method == "GET":
        data= models.jewel_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.jewel_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_jewel(request,subcategory):
    if request.method == "GET":
        data = models.jewel_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def get_single_jewelproduct(request,id,product_id):
    if request.method == "GET":
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login...............

@api_view(['GET'])
def user_get_all_jewelproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.jewel_productsmodel.objects.filter(jewel_id=id,status=True)
        alldataserializer= business_serializers.jewel_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_jewel(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_jewelproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.jewel_productsmodel.objects.filter(jewel_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.jewel_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)



# ....................food products............
@api_view(['GET'])
def all_foodproducts(request):
    if request.method == "GET":
        data= models.food_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.food_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def category_based_food(request,subcategory):
    if request.method == "GET":
        data = models.food_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_foodproduct(request,id,product_id):
    if request.method == "GET":
        data = models.food_productsmodel.objects.filter(food_id=id,product_id=product_id,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# .................after login...............

def user_get_all_foodproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.food_productsmodel.objects.filter(food_id=id,status=True)
        alldataserializer= business_serializers.food_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_food(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.food_productsmodel.objects.filter(food_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_foodproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.food_productsmodel.objects.filter(food_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.food_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


# ....................freshcuts products..........

@api_view(['GET'])
def all_freshcutproducts(request):
    if request.method == "GET":
        data= models.fresh_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.fresh_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_based_fresh(request,subcategory):
    if request.method == "GET":
        data = models.fresh_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_single_freshproduct(request,id,product_id):
    if request.method == "GET":
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login...............

@api_view(['GET'])
def user_get_all_freshproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.fresh_productsmodel.objects.filter(fresh_id=id,status=True)
        alldataserializer= business_serializers.fresh_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_fresh(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_freshproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.fresh_productsmodel.objects.filter(fresh_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.fresh_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# ....................dailymio products............


@api_view(['GET'])
def all_dmioproducts(request):
    if request.method == "GET":
        data= models.dmio_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.dmio_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_dmio(request,subcategory):
    if request.method == "GET":
 
        data = models.dmio_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_dmioproduct(request,id,product_id):
    if request.method == "GET":
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
# .................after login..............


@api_view(['GET'])
def user_get_all_dmioproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.dmio_productsmodel.objects.filter(dmio_id=id,status=True)
        alldataserializer= business_serializers.dmio_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_category_dmio(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_dmioproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.dmio_productsmodel.objects.filter(dmio_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.dmio_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# ....................pharmacy products............
@api_view(['GET'])
def all_pharmproducts(request):
    if request.method == "GET":
        data= models.pharmacy_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.pharmacy_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_pharm(request,subcategory):
    if request.method == "GET":

        data = models.pharmacy_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_pharmproduct(request,id,product_id):
    if request.method == "GET":
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK) 
# .................after login...............


@api_view(['GET'])
def user_get_all_pharmproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.pharmacy_productsmodel.objects.filter(pharm_id=id,status=True)
        alldataserializer= business_serializers.pharmacy_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_pharm(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_pharmproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.pharmacy_productsmodel.objects.filter(pharm_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.pharmacy_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# ....................dorigin products............


@api_view(['GET'])
def all_d_originalproducts(request):
    if request.method == "GET":

        data= models.d_original_productsmodel.objects.filter(status=True)
        alldataserializer= business_serializers.d_original_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def category_based_d_original(request,subcategory):
    if request.method == "GET":
 
        data = models.d_original_productsmodel.objects.filter(subcategory=subcategory,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_d_originalproduct(request,id,product_id):
    if request.method == "GET":
        data = models.d_original_productsmodel.objects.filter(d_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def d_original_district_products(request, id, district):
    if request.method == "GET":
        data = models.d_original_productsmodel.objects.filter(d_id=id, district=district)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

# .................after login...............

    
@api_view(['GET'])
def user_get_all_d_originalproducts(request,id,user_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data= models.d_original_productsmodel.objects.filter(d_id=id,status=True)
        alldataserializer= business_serializers.d_original_productlistserializer(data,many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_get_category_d_original(request,id,user_id,subcategory):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id) 
        print(user_id)
        data = models.d_original_productsmodel.objects.filter(d_id=id, subcategory=subcategory,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get_single_d_originalproduct(request,id,user_id,product_id):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.d_original_productsmodel.objects.filter(d_id=id, product_id=product_id,status=True)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def user_d_original_district_products(request, id,user_id, district):
    if request.method == "GET":
        user_id= models.End_Usermodel.objects.get(uid=user_id)
        print(user_id)
        data = models.d_original_productsmodel.objects.filter(d_id=id, district=district)
        alldataserializer = business_serializers.d_original_productlistserializer(data, many=True)
        return Response(data=alldataserializer.data, status=status.HTTP_200_OK)

#  Oreder Creation (Quick And Normal)
@api_view(["POST"])
def enduser_order_create(request,id,product_id,category):
    if request.method == "POST":
        user_data= models.End_Usermodel.objects.get(uid=id)
       
        order_id = end_user_extension.order_id_generate()
        while True:
            if id == order_id:
                order_id = end_user_extension.order_id_generate()
            else:
                break
        # shopping
        if category == "shopping" or category == "Shopping":
            
            products= models.shop_productsmodel.objects.get(product_id = product_id)
            shopping = models.shoppingmodel.objects.get(shop_id=products.shop_id)
            print(shopping.Business_id)
            business = models.Businessmodel.objects.get(uid=shopping.Business_id) 
            print(business) 
            if products:
                # selling_price = product_data.get("selling_price", 0)
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)
                print(total_amount)
            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'shop_product':products,
                'shop_id' : shopping,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Normal",
            }
            print(data)
            productorder = models.Product_Ordermodel(**data)
    
            # if basicdetailsserializer.is_valid():
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
            # else:
            #     print("serializer prblm")
            #     return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
        # Food
        elif category == "Food" or category == "food":
            products= models.food_productsmodel.objects.get(product_id = product_id)
            food = models.foodmodel.objects.get(food_id=products.food_id)
            print(food.Business_id)
            business = models.Businessmodel.objects.get(uid=food.Business_id) 
            print(business) 
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'food_product':products,
                'food_id' : food,
                'product_id':products.product_id,
                'business':business,
                
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
            }
            productorder = models.Product_Ordermodel(**data)
    
            # if basicdetailsserializer.is_valid():
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
            
        # FreshCut
        elif category == "Fresh_cuts" or category == "fresh_cuts":
            products= models.fresh_productsmodel.objects.get(product_id = product_id)
            freshcut = models.freshcutsmodel.objects.get(fresh_id=products.fresh_id)
            print(freshcut.Business_id)
            business = models.Businessmodel.objects.get(uid=freshcut.Business_id) 
            print(business) 
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'freshcut_product':products,
                'fresh_id' : freshcut,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
            }
            productorder = models.Product_Ordermodel(**data)
    
            # if basicdetailsserializer.is_valid():
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        # Pharmacy
        elif category == "Pharmacy"  or category == "pharmacy":
            products= models.pharmacy_productsmodel.objects.get(product_id = product_id)
            pharmacy = models.pharmacy_model.objects.get(pharm_id=products.pharm_id)
            print(pharmacy.Business_id)
            business = models.Businessmodel.objects.get(uid=pharmacy.Business_id) 
            print(business) 
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'pharmacy_product':products,
                'phram_id' : pharmacy,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
            }
            productorder = models.Product_Ordermodel(**data)
    
            # if basicdetailsserializer.is_valid():
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)

           
        # D-Original
        elif category == "d_original"  or category == "d_original": 
            products= models.d_original_productsmodel.objects.get(product_id = product_id)
            d_origin = models.d_originalmodel.objects.get(d_id=products.d_id)
            print(d_origin.Business_id)
            business = models.Businessmodel.objects.get(uid=d_origin.Business_id) 
            print(business) 
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'd_original_product':products,
                'd_id' : d_origin,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Normal",
            }
            productorder = models.Product_Ordermodel(**data)
    
            # if basicdetailsserializer.is_valid():
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        # Daily_MIO
        elif category == "daily_mio"  or category == "Daily_mio": 
            products= models.dmio_productsmodel.objects.get(product_id = product_id)
            daily_mio = models.dailymio_model.objects.get(dmio_id=products.dmio_id)
            print(daily_mio.Business_id)
            business = models.Businessmodel.objects.get(uid=daily_mio.Business_id) 
            print(business) 
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'dmio_product':products,
                'dmio_id' : daily_mio,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Quick",
            }
            productorder = models.Product_Ordermodel(**data)
    
            # if basicdetailsserializer.is_valid():
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        
        # Jewellery
        elif category == "jewellery"  or category == "Jewellery": 
            products= models.jewel_productsmodel.objects.get(product_id = product_id)
            jewellery = models.jewellerymodel.objects.get(jewel_id=products.jewel_id)
            print(jewellery.Business_id)
            business = models.Businessmodel.objects.get(uid=jewellery.Business_id) 
            print(business)          
            if products:
                # selling_price = product_data.get("selling_price", 0) 
                selling_price = products.product.get("selling_price") 
                total_amount = selling_price * int(request.POST['quantity'])
                print(selling_price)
                total_amount = math.floor(total_amount)

            else:
                pass
       
            data ={
                'end_user' :user_data,
                'order_id': order_id,
                'category_data':category,
                'track_id': end_user_extension.track_id_generate(),
                'quantity': request.POST["quantity"],
                'total_amount': total_amount,              
                'status': "pending",
                'jewel_product':products,
                'jewel_id' : jewellery,
                'product_id':products.product_id,
                'business':business,
                # 'payment_status' : request.POST['payment_status'],
                'delivery_type' : "Normal",
            }
            productorder = models.Product_Ordermodel(**data)
    
            productorder.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)

@api_view(["POST"])
def enduser_order_cancel(request,id,order_id):
    user=models.End_Usermodel.objects.get(uid = id)
    user_id=user.id
    print(user_id)
    order_data=get_object_or_404(models.Product_Ordermodel,order_id = order_id)
    product_user_id = order_data.end_user.id
    print(product_user_id)
    if order_data:
        if user_id == product_user_id:
            print(order_data.status)
            order_data.status="cancel"
            order_data.save()
            print(order_data.status)
            return Response("success",status=status.HTTP_200_OK)
        else:
            return Response({"user not found"},status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"no data"},status=status.HTTP_400_BAD_REQUEST)


