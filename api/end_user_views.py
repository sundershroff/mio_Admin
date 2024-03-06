from django.shortcuts import render
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
                    'full_name':request.data["full_name"],
                    'email': request.data["email"],
                    'phone_number': request.data["phone_number"],
                    'password': request.data["password"],
                    'created_date':str(x.strftime("%d"))+" "+str(x.strftime("%B"))+","+str(x.year)
                }
                print(datas)
                dataserializer = end_user_serializers.SignupSerializer(data=datas)
                print(dataserializer)
                
                if dataserializer.is_valid():            
                    dataserializer.save()
                    print("Valid Data")
                    end_user_extension.send_mail(datas['email'])
                    print("Email send")
                    return Response(datas['uid'], status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"Invalid Json Format (OR) Invalid Key"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def end_user_signin(request):
    try:
       
        try:
            if end_user_extension.validate_email(request.data['email']):
                if end_user_extension.get_user_id(request.data['email']):
                    return Response(end_user_extension.get_user_id(request.data['email']), status=status.HTTP_200_OK)
                
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