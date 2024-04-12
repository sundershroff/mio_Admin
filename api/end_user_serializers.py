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
    


class AddressSerializer(serializers.Serializer):
    doorno = serializers.CharField()
    area = serializers.CharField()
    landmark = serializers.CharField()
    place = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    pincode = serializers.CharField()

    def create(self, validated_data):
        return models.End_Usermodel.objects.create(address_data=validated_data)

    def update(self, instance, validated_data):
        instance.address_data = validated_data
        instance.save()
        return instance 
    
class TempAddressSerializer(serializers.Serializer):
    doorno = serializers.CharField()
    area = serializers.CharField()
    landmark = serializers.CharField()
    place = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    pincode = serializers.CharField()

    def create(self, validated_data):
        return models.End_Usermodel.objects.create(temp_address=validated_data)

    def update(self, instance, validated_data):
        instance.temp_address = validated_data
        instance.save()
        return instance
    

class product_orderSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    total_amount = serializers.CharField()
    # business_id = serializers.CharField()
    end_user_id = serializers.CharField()
    # delivery = serializers.CharField()
    # shop_id= serializers.CharField()
    shop_product_id = serializers.CharField()
    food_product_id = serializers.CharField()
    jewel_product_id = serializers.CharField()
    dmio_product_id =serializers.CharField()
    pharmacy_product_id = serializers.CharField()
    d_original_product_id = serializers.CharField()
    freshcut_product_id = serializers.CharField()
    status = serializers.CharField()    
    # delivery_date = serializers.CharField()
    # payment_status = serializers.CharField()
    delivery_type= serializers.CharField()
    category_data = serializers.CharField()
    # distance = serializers.CharField()
    # earn_perkm_amount = serializers.CharField()
    def create(self, data):
        return models.Product_Ordermodel.objects.create(
            order_id = data[' order_id'],
            track_id = data['track_id'],
            quantity = data['quantity'],
            total_amount = data['total_amount'],
            # business_id = data['business_id'],
            end_user_id = data['end_user_id'],
            shop_product_id = data['shop_product_id'],
            food_product_id =data['food_product_id'],
            jewel_product_id = data['jewel_product_id'],
            dmio_product_id = data['dmio_product_id'],
            pharmacy_product_id = data['pharmacy_product_id'],
            d_original_product_id = data['d_original_product_id'],
            freshcut_product_id = data['freshcut_product_id'],
            status = data['status'],
            delivery_type = data['delivery_type'],
            category_data = data['category_data'],

        )

class update_acc_serializer(serializers.Serializer):

    profile_picture=serializers.CharField()
    def update(self,instance,data):
       
        instance.profile_picture=data["profile_picture"]
        instance.save()
        return instance
