from rest_framework import serializers
from api import models


class EnduserSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    full_name=serializers.CharField()
    created_date=serializers.CharField()

class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    full_name=serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    created_date=serializers.CharField()
    def create(self, data):
        return models.End_Usermodel.objects.create(
            uid = data['uid'],
            full_name = data['full_name'],
            email = data['email'],
            phone_number = data['phone_number'],
            password = data['password'],
            created_date = data['created_date'],
        )