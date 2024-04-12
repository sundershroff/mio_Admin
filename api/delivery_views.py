from django.shortcuts import render
from api import business_serializers,end_user_serializers,delivery_serializers
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import delivery_extension
from rest_framework.decorators import api_view
from api import models
from mio_admin.models import comission_Editing
import json
import datetime
from django.http import JsonResponse
from datetime import date
from bson.json_util import dumps,loads
from pymongo import MongoClient
from geopy.distance import geodesic

from django.utils.timezone import now


client = MongoClient('localhost', 27017)
all_image_url = "http://127.0.0.1:3000/"

@api_view(['POST'])
def delivery_person_signup(request):
    try:
        if delivery_extension.validate_email(request.data.get('email')):
            return Response("User Already Exists", status=status.HTTP_302_FOUND)
        else:
            fs = FileSystemStorage()
         
            profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
            profile_picturepath = fs.save(f"api/delivery/profile_picture/"+profile_picture, request.FILES['profile_picture'])
            bank_passbok_pic = str(request.FILES['bank_passbok_pic']).replace(" ", "_")
            bank_passbok_pic_path = fs.save(f"api/delivery/bank_passbok_pic/"+bank_passbok_pic, request.FILES['bank_passbok_pic'])
            aadhar_pic = str(request.FILES['aadhar_pic']).replace(" ", "_")
            aadhar_pic_path = fs.save(f"api/delivery/aadhar_pic/"+aadhar_pic, request.FILES['aadhar_pic'])
            pan_pic = str(request.FILES['pan_pic']).replace(" ", "_")
            pan_pic_path = fs.save(f"api/delivery/pan_pic/"+pan_pic, request.FILES['pan_pic'])
            drlicence_pic = str(request.FILES['drlicence_pic']).replace(" ", "_")
            drlicence_pic_path = fs.save(f"api/delivery/drlicence_pic/"+drlicence_pic, request.FILES['drlicence_pic'])

        
            profile_picturepaths = all_image_url+fs.url(profile_picturepath)
            bank_passbok_pic_paths = all_image_url+fs.url(bank_passbok_pic_path)
            aadhar_pic_paths = all_image_url+fs.url(aadhar_pic_path)
            pan_pic_paths = all_image_url+fs.url(pan_pic_path)
            drlicence_pic_paths = all_image_url+fs.url(drlicence_pic_path)
            datas = {
                    'uid': delivery_extension.id_generate(),
                    'name':request.data["name"],
                    'phone_number': request.data['phone_number'],
                    'wp_number': request.data['wp_number'],
                    'email': request.data["email"],
                    'aadhar_number':request.data['aadhar_number'],                    
                    'driving_licensenum':request.data['driving_licensenum'],
                    'pan_number':request.data['pan_number'],                    
                    'profile_picture':profile_picturepaths,
                    'bank_name':request.data['bank_name'],
                    'acc_number':request.data['acc_number'],
                    'name_asper_passbook':request.data['name_asper_passbook'],
                    'ifsc_code':request.data['ifsc_code'],
                    'bank_passbok_pic':bank_passbok_pic_paths,
                    'aadhar_pic':aadhar_pic_paths,
                    'pan_pic':pan_pic_paths,
                    'drlicence_pic':drlicence_pic_paths,
                    'delivery_type':request.data['delivery_type'],
                    'region':request.data['region'],
                    'approve_status':"False",
            }

            dataserializer = delivery_serializers.SignupSerializer(data=datas)
            if dataserializer.is_valid():
                dataserializer.save()
                print("valid_data")
                return Response(datas['uid'], status=status.HTTP_200_OK)
            else:
                return Response(dataserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response({"Invalid Key": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def delivery_person_signin(request):
    try:
       
        try:
            if delivery_extension.verify_user(request.data['phone_number']):
                    if delivery_extension.get_user_id(request.data['phone_number']):
                        return Response(delivery_extension.get_user_id(request.data['phone_number']), status=status.HTTP_200_OK)
                    else:
                        return Response({"User Dosn't Exits"}, status=status.HTTP_401_UNAUTHORIZED)

            else:
                return Response({"Password Is Incorrect"}, status=status.HTTP_403_FORBIDDEN)
        
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def all_delivery_person_data(request):
    if request.method == "GET":
        data=models.Delivery_model.objects.all()
        serializers=delivery_serializers.DeliverypersonSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)



# one person data    
@api_view(["GET"])
def single_delivery_person_data(request,id):
    if request.method == "GET":
        data=models.Delivery_model.objects.get(uid=id)
        print(data)
        serializers=delivery_serializers.DeliverypersonSerializer(data,many=False)
        print(serializers)
        return Response(data=serializers.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def delivery_person_update(request,id):
    if request.method=="POST":
        fs=FileSystemStorage
        # print(request.data)
        # print(request.FILES)
        d_data = models.Delivery_model.objects.get(uid=id)
        print(d_data)
        datas = models.Delivery_model.objects.filter(uid=id).values()[0]
        print(datas)

        if "profile_picture" in request.FILES:
            profile_picture = str(request.FILES['profile_picture']).replace(" ","_")
            profile_picture_path = fs.save(f"api/delivery/{id}/profile_picture/"+profile_picture, request.FILES["profile_picture"])
            profile_picturepaths = all_image_url+fs.url(profile_picture_path)
        else:
            profile_picturepaths = datas["profile_picture"]
            print(profile_picturepaths) 
        if "bank_passbok_pic" in request.FILES:
            bank_passbok_pic = str(request.FILES["pan_file"]).replace(" ","_")
            bank_passbok_pic_path = fs.save(f"api/delivery/{id}/bank_passbok_pic/"+bank_passbok_pic,request.FILES["bank_passbok_pic"])
            bank_passbok_pic_paths = all_image_url+fs.url(bank_passbok_pic_path)
        else:
            bank_passbok_pic_paths = datas["bank_passbok_pic"]
            print(bank_passbok_pic_paths)
        if "aadhar_pic" in request.FILES:
            aadhar_pic = str(request.FILES["aadhar_pic"]).replace(" ","_")
            aadhar_pic_path = fs.save(f"api/delivery/{id}/aadhar_pic/"+aadhar_pic,request.FILES["aadhar_pic"])
            aadhar_pic_paths = all_image_url+fs.url(aadhar_pic_path)
        else:
            aadhar_pic_paths = datas["aadhar_pic"]
            print(aadhar_pic_paths)
        if "pan_pic" in request.FILES:
            pan_pic = str(request.FILES["pan_pic"]).replace(" ","_")
            pan_pic_path = fs.save(f"api/delivery/{id}/pan_pic/"+pan_pic,request.FILES["pan_pic"])
            pan_pic_paths = all_image_url+fs.url(pan_pic_path)
        else:
            pan_pic_paths = datas["pan_pic"]
            print(pan_pic_paths)
        if "drlicence_pic" in request.FILES:
            drlicence_pic = str(request.FILES["drlicence_pic"]).replace(" ","_")
            drlicence_pic_path = fs.save(f"api/delivery/{id}/drlicence_pic/"+drlicence_pic,request.FILES["drlicence_pic"])
            drlicence_pic_paths = all_image_url+fs.url(drlicence_pic_path)
        else:
            drlicence_pic_paths = datas["drlicence_pic"]
            print(drlicence_pic_paths)
        print(request.data)
        data= {
            'name':request.data['name'],
            'phone_number':request.data['phone_number'],
            'wp_number': request.data['wp_number'],
            'email': request.data["email"],
            'aadhar_number':request.data['aadhar_number'],                    
            'driving_licensenum':request.data['driving_licensenum'],
            'pan_number':request.data['pan_number'],                    
            'profile_picture':profile_picturepaths,
            'bank_name':request.data['bank_name'],
            'acc_number':request.data['acc_number'],
            'name_asper_passbook':request.data['name_asper_passbook'],
            'ifsc_code':request.data['ifsc_code'],
            'bank_passbok_pic':bank_passbok_pic_paths,
            'aadhar_pic':aadhar_pic_paths,
            'pan_pic':pan_pic_paths,
            'drlicence_pic':drlicence_pic_paths,
            'delivery_type':request.data['delivery_type'],
            'region':request.data['region']
        }
        print(data,"data")
        dataserializer = delivery_serializers.deliveryperson_edit_serializer(instance=d_data, data=data, partial=True)
        print(dataserializer)
        if dataserializer.is_valid():
            dataserializer.save()
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)






@api_view(["GET"])
def delivery_get_normalproduct_order(request, id,region,delivery_person_latitude,delivery_person_longitude):
    if models.Delivery_model.objects.filter(uid=id).exists():
    

        # Get all quick delivery persons in the region
        quick_delivery_persons = models.Delivery_model.objects.filter(region=region, delivery_type='Normal')

        # Calculate distance and sort delivery persons by distance
        orders = None
        for delivery_person in quick_delivery_persons:
            # distance_to_delivery_person = geodesic((delivery_person_latitude, delivery_person_longitude), (delivery_person.latitude, delivery_person.longitude)).kilometers
            distance_to_delivery_person = geodesic(("8.293231018581114", "77.25760012886072"), ("8.27934420482011", "77.26528197561439")).kilometers
            print(distance_to_delivery_person)
            orders = models.Product_Ordermodel.objects.filter(
                delivery_type='Quick',
               
                status='accepted'
            )
            if orders:
                break  # If orders are found, break the loop

        if orders:
            order_data = []
            for order in orders:
                if order.shop_product:  
                    print(order.shop_product.product)
                    order_data.append(order.shop_product.product)
                elif order.jewel_product:  
                    print(order.jewel_product.product)
                    order_data.append(order.jewel_product.product)
                elif order.d_original_product:  
                    print(order.d_original_product.product)
                    order_data.append(order.d_original_product.product)
                else:
                    print("Unknown product type")

            order_data_dict = {item['product_id']: item for item in order_data}
            return Response(order_data_dict, status=status.HTTP_200_OK)
        else:
            return Response("No quick orders found for this region", status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("Business not found", status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def delivery_product_order_status_accept(request,id,product_id,order_id):
    try:
        delivery = models.Delivery_model.objects.get(uid=id)
        
        product_orders = models.Product_Ordermodel.objects.filter(product_id=product_id, order_id=order_id)
        print(product_orders)
        if product_orders.exists():
            for product_order in product_orders:
                # Update the status field with the new value
                product_order.status = "order-confirmed"
                product_order.save()
            return Response("Status updated successfully", status=status.HTTP_200_OK)
        else:
            return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)
    except:
        return Response("Product order not found", status=status.HTTP_404_NOT_FOUND)





# from geopy.distance import geodesic

# @api_view(["POST"])
# def user_order_product(request):
#   Shop= models.Product_Ordermodel.objects.get(shop_id= id)
    
#     # Get latitude and longitude from request
#     latitude = request.POST.get('latitude')
#     longitude = request.POST.get('longitude')

#     data = {        
#         'latitude': latitude,
#         'longitude': longitude,
#     }

#     # Calculate user distance based on latitude and longitude
#     user_location = (latitude, longitude) if latitude and longitude else None

#     if user_location:
#         shop_location = (shop.latitude, shop.longitude) 
#  # Assuming latitude and longitude fields in shoppingmodel. 

#         distance = geodesic(user_location, shop_location).kilometers
#         data['distance_to_shop'] = distance
  
#     basicdetailsserializer = end_user_serializers.user_order_createserializers(data=data)
    
#     if basicdetailsserializer.is_valid():
#         basicdetailsserializer.save()
#         print("Valid Data")
#         return Response(id, status=status.HTTP_200_OK)
#     else:
#         print("serializer problem")
#         return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)
