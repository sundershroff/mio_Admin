from rest_framework import serializers
from api import models


class DeliverypersonSerializer(serializers.Serializer):
    uid = serializers.CharField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    wp_number = serializers.CharField()
    email = serializers.EmailField()
    aadhar_number = serializers.CharField()
    pan_number = serializers.CharField()
    driving_licensenum = serializers.CharField()
    profile_picture = serializers.CharField()
    bank_name = serializers.CharField()
    acc_number = serializers.CharField()
    name_asper_passbook = serializers.CharField()
    ifsc_code = serializers.CharField()
    bank_passbok_pic = serializers.CharField()
    aadhar_pic = serializers.CharField()
    pan_pic = serializers.CharField()
    drlicence_pic = serializers.CharField()
    delivery_type = serializers.CharField()
    approve_status = serializers.CharField()
    today_earnings = serializers.CharField()
    region =serializers.CharField()
       


class SignupSerializer(serializers.Serializer):
    # Your fields here
    uid = serializers.CharField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    wp_number = serializers.CharField()
    email = serializers.EmailField()
    aadhar_number = serializers.CharField()
    pan_number = serializers.CharField()
    driving_licensenum = serializers.CharField()
    profile_picture = serializers.CharField()
    bank_name = serializers.CharField()
    acc_number = serializers.CharField()
    name_asper_passbook = serializers.CharField()
    ifsc_code = serializers.CharField()
    bank_passbok_pic = serializers.CharField()
    aadhar_pic = serializers.CharField()
    pan_pic = serializers.CharField()
    drlicence_pic = serializers.CharField()
    delivery_type = serializers.CharField()
    region =serializers.CharField()
    approve_status =serializers.CharField()
    def create(self, data):
        return models.Delivery_model.objects.create(**data
            # uid = data['uid'],
            # name = data['name'],
            # phone_number = data['phone_number'],
            # wp_number = data['wp_number'],
            # email = data['email'],
            # aadhar_number = data['aadhar_number'],
            # pan_number = data['pan_number'],
            # driving_licensenum = data['driving_licensenum'],
            # profile_picture = data['profile_picture'],
            # bank_name = data['bank_name'],
            # acc_number = data['acc_number'],
            # name_asper_passbook = data['name_asper_passbook'],
            # ifsc_code = data['ifsc_code'],
            # bank_passbok_pic = data['bank_passbok_pic'],
            # aadhar_pic = data['aadhar_pic'],
            # pan_pic = data['pan_pic'],
            # drlicence_pic = data['drlicence_pic'],
            # delivery_type = data['delivery_type'],
           

        )


class deliveryperson_edit_serializer(serializers.Serializer):

    name = serializers.CharField()
    phone_number = serializers.CharField()
    wp_number = serializers.CharField()
    email = serializers.EmailField()
    aadhar_number = serializers.CharField()
    driving_licensenum = serializers.CharField()
    pan_number = serializers.CharField()
    profile_picture = serializers.CharField()
    bank_name = serializers.CharField()
    acc_number = serializers.CharField()
    name_asper_passbook = serializers.CharField()
    ifsc_code = serializers.CharField()
    bank_passbok_pic = serializers.CharField()
    aadhar_pic = serializers.CharField()
    pan_pic = serializers.CharField()
    drlicence_pic = serializers.CharField()
    delivery_type = serializers.CharField()
    region = serializers.CharField()
    # today_earnings = serializers.CharField()
    def update(self,instance,data):
        instance.name = data["name"]
        instance.phone_number = data["phone_number"]
        instance.wp_number = data["wp_number"]
        instance.email = data["email"]
        instance.aadhar_number = data["aadhar_number"]
        instance.driving_licensenum = data["driving_licensenum"]
        instance.pan_number = data["pan_number"]
        instance.profile_picture = data["profile_picture"]
        instance.bank_name = data["bank_name"]
        instance.acc_number = data["acc_number"]
        instance.name_asper_passbook = data["name_asper_passbook"]
        instance.ifsc_code = data["ifsc_code"]
        instance.bank_passbok_pic = data["bank_passbok_pic"]
        instance.aadhar_pic = data["aadhar_pic"]
        instance.pan_pic = data["pan_pic"]
        instance.drlicence_pic = data["drlicence_pic"]
        instance.delivery_type = data["delivery_type"]
        instance.region =data['region']
        
        # instance.today_earnings = data['today_earnings']
        instance.save()
        return instance

    




