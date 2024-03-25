from django.shortcuts import render
from api import business_serializers,end_user_serializers,delivery_serializers
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework import status,generics
from django.core.files.storage import FileSystemStorage
from api import delivery_extension
from rest_framework.decorators import api_view
from api import models
import json
import datetime
from bson.json_util import dumps,loads
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
all_image_url = "http://127.0.0.1:3000/"
x = datetime.datetime.now()

@api_view(['POST'])
def delivery_person_signup(request):
    try:
        try:
            if delivery_extension.validate_email(request.data['email']):
                return Response("User Already Exists", status=status.HTTP_302_FOUND)
            else:
                x = datetime.datetime.now()
                datas = {
                    'uid': delivery_extension.id_generate(),
                    'otp': delivery_extension.otp_generate(),
                    'full_name':request.data["full_name"],
                    'email': request.data["email"],
                    'phone_number': request.data['phone_number'],
                    'password': request.data["password"],
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = delivery_serializers.SignupSerializer(data=datas)
                print(dataserializer)
                
                if dataserializer.is_valid():            
                    dataserializer.save()
                    print("Valid Data")
                    delivery_extension.send_mail(datas['email'], datas['otp'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def delivery_person_otp(request, id):
    try:
        try:
            if delivery_extension.validate_otp(id, int(request.data['user_otp'])):
                try:
                    userData = models.Delivery_model.objects.get(uid=id)
                    print(userData)
                    serializer_validate = delivery_serializers.OTPSerializer(
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
def delivery_person_signin(request):
    try:
       
        try:
            if delivery_extension.validate_email(request.data['email']):
                if delivery_extension.verify_user(request.data['email'], request.data['password']):
                    if delivery_extension.verify_user_otp(request.data['email']):
                        if delivery_extension.get_user_id(request.data['email']):
                            return Response(delivery_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
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
def all_delivery_person_data(request):
    if request.method == "GET":
        data=models.Delivery_model.objects.all()
        serializers=delivery_serializers.DeliverypersonSerializer(data,many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def deliveryresend_otp(request,id):

    try:
        try:
            new_otp = delivery_extension.otp_generate()
            user = models.Delivery_model.objects.get(uid=id)
            email = user.email 
            print(f"Email: {email}")
            delivery_extension.send_mail(email, new_otp)
            user.otp = new_otp
            user.save()
            return Response({"New OTP": new_otp, "Email": email}, status=status.HTTP_200_OK)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def delivery_forget_password(request):

    try:
        try:
            print(request.POST)
            if delivery_extension.validate_email(request.data['email']):
                Data = models.Delivery_model.objects.get(email=request.data['email'])

                data1={
                    'email':request.data['email'],
                    'password':request.data['password']
                }
                print(data1)
                basicdetailsserializer = delivery_serializers.forget_password_serializer(instance=Data, data=data1,partial=True)
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
def delivery_profile_picture(request,id):
    try:
        print(request.FILES['profile_picture'])
        fs = FileSystemStorage()
        userdata = models.Delivery_model.objects.get(uid=id)
        
        profile_picture = str(request.FILES['profile_picture']).replace(" ", "_")
     
        path = fs.save(f"api/delivery/{id}/profile_picture/"+profile_picture, request.FILES['profile_picture'])
        full_path = all_image_url+fs.url(path)
        print(full_path)

        data = {          
            'profile_picture': full_path           
        }

        print(data)
        basicdetailsserializer = delivery_serializers.profile_picture_Serializer(
            instance=userdata, data=data, partial=True)
        if basicdetailsserializer.is_valid():
            basicdetailsserializer.save()
            print("Valid Data")
            return Response(id, status=status.HTTP_200_OK)
        else:
            return Response({"sserializer issue"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return Response({"Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)




