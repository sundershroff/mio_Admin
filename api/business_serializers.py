from api.models import Businessmodel,shoppingmodel,jewellerymodel,foodmodel,freshcutsmodel,pharmacy_model,d_originalmodel,dailymio_model
from rest_framework import serializers
from api import models


class BusinessSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    otp = serializers.IntegerField()
    full_name=serializers.CharField()
    created_date=serializers.CharField()
    user_otp = serializers.IntegerField()
    profile_picture = serializers.CharField()

class SignupSerializer(serializers.Serializer):
    uid = serializers.CharField()
    otp = serializers.IntegerField()
    full_name=serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    created_date=serializers.CharField()
    def create(self, data):
        return Businessmodel.objects.create(
            uid = data['uid'],
            otp = data['otp'],
            full_name = data['full_name'],
            email = data['email'],
            phone_number = data['phone_number'],
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

# shop_order

class shop_order_serializer(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    shop_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()


# shopping

class shopping_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    shop_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    hub = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def create(self,data):
        return shoppingmodel.objects.create(
            Business_id = data['Business_id'],
            shop_id = data['shop_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            hub = data['hub'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class shopping_list_serializer(serializers.Serializer):
    shop_id = serializers.CharField()
    Business_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    hub = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()
    total_revenue = serializers.CharField()
    monthly_revenue = serializers.CharField()
class shopping_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    hub = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.hub = data['hub']
        instance.pin_number = data['pin_number']
        instance.aadhar_number = data['aadhar_number']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance

# shopping products
class shop_electronicsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_electronicsmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_electronicslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()
class shop_mobileserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_mobilemodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_mobilelistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()
class shop_furnitureserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_furnituremodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )

class shop_furniturelistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_autoaccessoriesserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_autoaccessoriesmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_autoaccessorieslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_kitchenserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_kitchenmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_kitchenlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_fashionserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_fashionmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_fashionlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()
class shop_appliancesserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_appliancesmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_applianceslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()
class shop_groceriesserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_groceriesmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_grocerieslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_petsuppliesserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_petsuppliesmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_petsupplieslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_toysserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_toysmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_toysserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_sportsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_sportsmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_sportslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_healthcareserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_healthcaremodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_healthcarelistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_booksserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_booksmodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_bookslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

class shop_personalcareserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    def create(self,data):
        return models.shop_personalcaremodel.objects.create(

            product_id = data['product_id'],
            shop_id = data['shop_id']
        )
class shop_personalcarelistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    shop_id = serializers.CharField()
    status=serializers.BooleanField()

# jewellery

class jewellery_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    jewel_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    hub = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()


    def create(self,data):
        return jewellerymodel.objects.create(
            Business_id = data['Business_id'],
            jewel_id = data['jewel_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            hub = data['hub'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class jewellery_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    jewel_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    hub = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

class jewellery_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    hub = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.hub = data['hub']
        instance.pin_number = data['pin_number']
        instance.aadhar_number = data['aadhar_number']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance   

# jewellery products
class jewel_goldserializer(serializers.Serializer):
    product_id = serializers.CharField()
    jewel_id = serializers.CharField()
    def create(self,data):
        return models.jewel_goldmodel.objects.create(

            product_id = data['product_id'],
            jewel_id = data['jewel_id']
        )
class jewel_goldlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    jewel_id = serializers.CharField()
    status=serializers.BooleanField()
class jewel_silverserializer(serializers.Serializer):
    product_id = serializers.CharField()
    jewel_id = serializers.CharField()
    def create(self,data):
        return models.jewel_silvermodel.objects.create(

            product_id = data['product_id'],
            jewel_id = data['jewel_id']
        )
class jewel_silverlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    jewel_id = serializers.CharField()
    status=serializers.BooleanField()


class jewel_order_serializer(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    jewel_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()

# food

class food_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    food_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def create(self,data):
        return foodmodel.objects.create(
            Business_id = data['Business_id'],
            food_id = data['food_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class food_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    food_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number=serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

class food_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pin_number = data['pin_number']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        instance.region = data['region']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance

# foodproducts
class food_tiffenserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_tiffenmodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )

class food_tiffenlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_mealsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_mealsmodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_mealslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_biriyaniserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_biriyanimodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_biriyanilistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_chickenbiriyaniserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_chickenbiriyanimodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_chickenbiriyanilistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_beefserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_beefmodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_beeflistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_chineseserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_chinesemodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_chineselistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_pizzaserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_pizzamodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
        
class food_pizzalistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_teacoffeserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_teacoffemodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_teacoffelistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_icecreamserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_icecreammodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_icecreamlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_firedchickenserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_firedchickenmodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_firedchickenlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_burgerserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_burgermodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_burgerlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_cakeserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_cakemodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
class food_cakelistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()
class food_bakeryserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    def create(self,data):
        return models.food_bakerymodel.objects.create(

            product_id = data['product_id'],
            food_id = data['food_id']
        )
    
class food_bakerylistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    food_id = serializers.CharField()
    status=serializers.BooleanField()


class food_orderserializers(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    food_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()



# freshcuts
class freshcuts_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    fresh_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def create(self,data):
        return freshcutsmodel.objects.create(
            Business_id = data['Business_id'],
            fresh_id = data['fresh_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class freshcuts_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    fresh_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

class freshcuts_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pin_number = data['pin_number']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        instance.region = data['region']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance


class fresh_chickenserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_chickenmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_chickenlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_muttonserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_muttonmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_muttonlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_beefserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_beefmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
        
class fresh_beeflistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_fishseafoodserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_fishseafoodmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_fishseafoodlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_dryfishserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_dryfishmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_dryfishlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_prawnsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_prawnsmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_prawnslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_eggserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_eggmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_egglistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_pondfishserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_pondfishmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
        
class fresh_pondfishlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_meatmasalaserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_meatmasalamodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_meatmasalalistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_comboserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_combomodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
        
class fresh_combolistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()
class fresh_choppedvegserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    def create(self,data):
        return models.fresh_choppedvegmodel.objects.create(

            product_id = data['product_id'],
            fresh_id = data['fresh_id']
        )
class fresh_choppedveglistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    fresh_id = serializers.CharField()
    status=serializers.BooleanField()

class fresh_orderserializers(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    fresh_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()



# dailymio

class dailymio_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    dmio_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def create(self,data):
        return dailymio_model.objects.create(
            Business_id = data['Business_id'],
            dmio_id = data['dmio_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class dailymio_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    dmio_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

class dailymio_edit_serializer(serializers.Serializer):

    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pin_number = data['pin_number']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        instance.region = data['region']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance

class dmio_groceryserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_grocerymodel.objects.create(

            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
        
class dmio_grocerylistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()
class dmio_meatserializer(serializers.Serializer):
    producdt_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_meatmodel.objects.create(

            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
class dmio_meatlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()
class dmio_fishserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_fishmodel.objects.create(

            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
        
class dmio_fishlistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()
class dmio_eggsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_eggsmodel.objects.create(

            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
        
class dmio_eggslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()
class dmio_fruitsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_fruitsmodel.objects.create(
            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
class dmio_fruitslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()
class dmio_vegitablesserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_vegitablesmodel.objects.create(

            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
class dmio_vegitableslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()
class dmio_dairyserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    def create(self,data):
        return models.dmio_dairymodel.objects.create(
            product_id = data['product_id'],
            dmio_id = data['dmio_id']
        )
class dmio_dairylistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    dmio_id = serializers.CharField()
    status=serializers.BooleanField()

class dorigin_orderserializers(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    d_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()
# pharmacy
class pharmacy_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    pharm_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def create(self,data):
        return pharmacy_model.objects.create(
            Business_id = data['Business_id'],
            pharm_id = data['pharm_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            fssa = data['fssa'],
            region = data['region'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class pharmacy_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    pharm_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

class pharmacy_edit_serializer(serializers.Serializer):
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    region = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pin_number = data['pin_number']
        instance.aadhar_number = data['aadhar_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        instance.region = data['region']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance


class pharmacy_allopathicserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    def create(self,data):
        return models.pharmacy_allopathicmodel.objects.create(
            product_id = data['product_id'],
            pharm_id = data['pharm_id']
        )
class pharmacy_allopathiclistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    status=serializers.BooleanField()
class pharmacy_ayurvedicserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    def create(self,data):
        return models.pharmacy_ayurvedicmodel.objects.create(
            product_id = data['product_id'],
            pharm_id = data['pharm_id']
        )
class pharmacy_ayurvediclistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    status=serializers.BooleanField()
class pharmacy_siddhaserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    def create(self,data):
        return models.pharmacy_siddhamodel.objects.create(
            product_id = data['product_id'],
            pharm_id = data['pharm_id']
        )
class pharmacy_siddhalistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    status=serializers.BooleanField()
class pharmacy_unaniserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    def create(self,data):
        return models.pharmacy_unanimodel.objects.create(
            product_id = data['product_id'],
            pharm_id = data['pharm_id']
        )
class pharmacy_unanilistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    status=serializers.BooleanField()
class pharmacy_herbaldrinksserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    def create(self,data):
        return models.pharmacy_herbaldrinksmodel.objects.create(
            product_id = data['product_id'],
            pharm_id = data['pharm_id']
        )
class pharmacy_herbaldrinkslistserializer(serializers.Serializer):
    product_id = serializers.CharField()
    pharm_id = serializers.CharField()
    status=serializers.BooleanField()


class pharmacy_orderserializers(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    pharm_id= serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()
# d_originalmodel
class d_original_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    d_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    fssa = serializers.CharField()
    hub = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def create(self,data):
        return d_originalmodel.objects.create(
            Business_id = data['Business_id'],
            d_id = data['d_id'],
            seller_name = data['seller_name'],
            business_name = data['business_name'],
            pan_number = data['pan_number'],
            gst = data['gst'],
            contact = data['contact'],
            alternate_contact = data['alternate_contact'],
            pin_number = data['pin_number'],
            aadhar_number = data['aadhar_number'],
            fssa = data['fssa'],
            hub = data['hub'],
            door_number =data['door_number'],
            street_name = data['street_name'],
            area = data['area'],
            pin_your_location = data['pin_your_location'],
            name = data['name'],
            account_number = data['account_number'],
            ifsc_code = data['ifsc_code'],
            upi_id = data['upi_id'],
            gpay_number = data['gpay_number'],
            aadhar = data['aadhar'],
            pan_file = data['pan_file'],
            profile = data['profile'],
            bank_passbook = data['bank_passbook'],
            gst_file = data['gst_file'],
            date = data['date']
        )

class d_original_list_serializer(serializers.Serializer):
    Business_id = serializers.CharField()
    d_id = serializers.CharField()
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    hub = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

class d_original_edit_serializer(serializers.Serializer):
    seller_name = serializers.CharField()
    business_name = serializers.CharField()
    pan_number = serializers.CharField()
    gst = serializers.CharField()
    contact = serializers.CharField()
    alternate_contact = serializers.CharField()
    pin_number = serializers.CharField()
    aadhar_number = serializers.CharField()
    door_number = serializers.CharField()
    street_name = serializers.CharField()
    area = serializers.CharField()
    fssa = serializers.CharField()
    hub = serializers.CharField()
    pin_your_location = serializers.CharField()      
    name = serializers.CharField()
    account_number = serializers.CharField()
    ifsc_code = serializers.CharField()
    upi_id = serializers.CharField()
    gpay_number = serializers.CharField()
    aadhar = serializers.CharField()
    pan_file = serializers.CharField()
    profile = serializers.CharField()
    bank_passbook = serializers.CharField()
    gst_file = serializers.CharField()
    date = serializers.CharField()

    def update(self,instance,data):
        instance.seller_name = data['seller_name']
        instance.business_name = data['business_name']
        instance.pan_number = data['pan_number']
        instance.gst = data['gst']
        instance.contact = data['contact']
        instance.alternate_contact = data['alternate_contact']
        instance.pin_number = data['pin_number']
        instance.door_number = data['door_number']
        instance.street_name = data['street_name']
        instance.area = data['area']
        instance.fssa = data['fssa']
        instance.hub = data['hub']
        instance.pin_your_location = data['pin_your_location']
        instance.name = data['name']
        instance.account_number = data['account_number']
        instance.ifsc_code = data['ifsc_code']
        instance.upi_id = data['upi_id']
        instance.gpay_number = data['gpay_number']
        instance.aadhar = data['aadhar']
        instance.pan_file = data['pan_file']
        instance.profile = data['profile']
        instance.bank_passbook = data['bank_passbook']
        instance.gst_file = data['gst_file']
        instance.date = data['date']
        instance.save()
        return instance


class d_originalproductsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    d_id = serializers.CharField()
    def create(self,data):
        return models.d_originalproductsmodel.objects.create(
            product_id = data['product_id'],
            d_id = data['d_id']
        )

class d_originalproductsserializer(serializers.Serializer):
    product_id = serializers.CharField()
    d_id = serializers.CharField()
    status=serializers.BooleanField()

class daily_orderserializers(serializers.Serializer):
    order_id =serializers.CharField()
    track_id = serializers.CharField()
    quantity = serializers.CharField()
    order_date =serializers.DateField()
    total_amount = serializers.CharField()
    business_id = serializers.CharField()
    dmio_id = serializers.CharField()
    product_id = serializers.CharField()
    e_user_id = serializers.CharField()
    status = serializers.CharField()
