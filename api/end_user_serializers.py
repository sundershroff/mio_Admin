from rest_framework import serializers
from api import models


class EnduserSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    user_otp = serializers.IntegerField()
    profile_picture = serializers.CharField()
    full_name=serializers.CharField()
    created_date=serializers.CharField()

class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    full_name=serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    otp = serializers.IntegerField()
    password = serializers.CharField()
    created_date=serializers.CharField()
    def create(self, data):
        return models.End_Usermodel.objects.create(
            uid = data['uid'],
            full_name = data['full_name'],
            email = data['email'],
            phone_number = data['phone_number'],
            otp = data['otp'],
            password = data['password'],
            created_date = data['created_date'],
        )
    
class OTPSerializer(serializers.Serializer):
    user_otp = serializers.IntegerField()
    
    def update(self, instance, data):
        instance.user_otp = data['user_otp']
        instance.save()
        return instance
    
class forget_password_serializer(serializers.Serializer):
    password = serializers.CharField()
    
    def update (self,instance,data):
        instance.password=data["password"]
        instance.save()
        return instance


class profile_picture_Serializer(serializers.Serializer):
    profile_picture = serializers.CharField()
    
    def update(self, instance, data):
        instance.profile_picture = data['profile_picture']
        instance.save()
        return instance
    

class forget_password_serializer(serializers.Serializer):
    password = serializers.CharField()
    
    def update (self,instance,data):
        instance.password=data["password"]
        instance.save()
        return instance