from django.db import models
from django.utils import timezone

import datetime
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

class Businessmodel(models.Model):
    # User ID
    uid = models.TextField()
    # Signup
    email = models.EmailField()
    phone_number = models.TextField(null=True) 
    password = models.TextField()
    otp = models.IntegerField()
    user_otp = models.IntegerField(null=True)
    full_name=models.TextField()
    created_date=models.TextField(null=True)
    
    profile_picture = models.TextField(null=True)

class shoppingmodel(models.Model):
    shop_id = models.TextField(null=True)
    Business_id = models.TextField()
    seller_name = models.TextField()
    business_name = models.TextField()
    pan_number = models.TextField()
    gst = models.TextField()
    contact = models.TextField()
    alternate_contact = models.TextField()
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    region = models.TextField(null=True)
    aadhar_number = models.TextField(null=True)
    pin_number = models.TextField()
    pin_your_location = models.TextField()
    name = models.TextField()
    account_number = models.TextField()
    ifsc_code = models.TextField()
    upi_id = models.TextField()
    gpay_number = models.TextField()
    aadhar = models.TextField()
    pan_file = models.TextField()
    profile = models.TextField()
    bank_passbook = models.TextField()
    gst_file = models.TextField()
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)




class jewellerymodel(models.Model):
    jewel_id = models.TextField(null=True)
    Business_id = models.TextField()
    seller_name = models.TextField()
    business_name = models.TextField()
    pan_number = models.TextField()
    gst = models.TextField()
    contact = models.TextField()
    alternate_contact = models.TextField()
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    region = models.TextField(null=True)
    aadhar_number=models.TextField(null=True)
    pin_number = models.TextField()
    pin_your_location = models.TextField()
    name = models.TextField()
    account_number = models.TextField()
    ifsc_code = models.TextField()
    upi_id = models.TextField()
    gpay_number = models.TextField()
    aadhar = models.TextField()
    pan_file = models.TextField()
    profile = models.TextField()
    bank_passbook = models.TextField()
    gst_file = models.TextField()
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

class foodmodel(models.Model):
    food_id = models.TextField(null=True)
    Business_id = models.TextField()
    seller_name = models.TextField()
    business_name = models.TextField()
    pan_number = models.TextField()
    gst = models.TextField()
    contact = models.TextField()
    alternate_contact = models.TextField()
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    aadhar_number=models.TextField(null=True)
    pin_number = models.TextField()
    fssa = models.TextField()
    region = models.TextField(null=True)
    pin_your_location = models.TextField()
    name = models.TextField()
    account_number = models.TextField()
    ifsc_code = models.TextField()
    upi_id = models.TextField()
    gpay_number = models.TextField()
    aadhar = models.TextField()
    pan_file = models.TextField()
    profile = models.TextField()
    bank_passbook = models.TextField()
    gst_file = models.TextField()
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

class freshcutsmodel(models.Model):
    fresh_id = models.TextField(null=True)
    Business_id = models.TextField()
    seller_name = models.TextField()
    business_name = models.TextField()
    pan_number = models.TextField()
    gst = models.TextField()
    contact = models.TextField()
    alternate_contact = models.TextField()
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    aadhar_number=models.TextField(null=True)
    pin_number = models.TextField()
    fssa = models.TextField()
    region = models.TextField(null=True)
    pin_your_location = models.TextField()
    name = models.TextField()
    account_number = models.TextField()
    ifsc_code = models.TextField()
    upi_id = models.TextField()
    gpay_number = models.TextField()
    aadhar = models.TextField()
    pan_file = models.TextField()
    profile = models.TextField()
    bank_passbook = models.TextField()
    gst_file = models.TextField()
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

class dailymio_model(models.Model):
    dmio_id = models.TextField(null=True)
    Business_id = models.TextField(null=True)
    seller_name = models.TextField(null=True)
    business_name = models.TextField(null=True)
    pan_number = models.TextField(null=True)
    gst = models.TextField(null=True)
    contact = models.TextField(null=True)
    alternate_contact = models.TextField(null=True)
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    aadhar_number=models.TextField(null=True)
    pin_number = models.TextField(null=True)
    fssa = models.TextField(null=True)
    region = models.TextField(null=True)
    pin_your_location = models.TextField(null=True)
    name = models.TextField(null=True)
    account_number = models.TextField(null=True)
    ifsc_code = models.TextField(null=True)
    upi_id = models.TextField(null=True)
    gpay_number = models.TextField(null=True)
    aadhar = models.TextField(null=True)
    pan_file = models.TextField(null=True)
    profile = models.TextField(null=True)
    bank_passbook = models.TextField(null=True)
    gst_file = models.TextField(null=True)
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

class pharmacy_model(models.Model):
    pharm_id = models.TextField(null=True)
    Business_id = models.TextField()
    seller_name = models.TextField()
    business_name = models.TextField()
    pan_number = models.TextField()
    gst = models.TextField()
    contact = models.TextField()
    alternate_contact = models.TextField()
    pin_number = models.TextField()
    aadhar_number=models.TextField(null=True)
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    fssa = models.TextField()
    region = models.TextField(null=True)
    pin_your_location = models.TextField()
    name = models.TextField()
    account_number = models.TextField()
    ifsc_code = models.TextField()
    upi_id = models.TextField()
    gpay_number = models.TextField()
    aadhar = models.TextField()
    pan_file = models.TextField()
    profile = models.TextField()
    bank_passbook = models.TextField()
    gst_file = models.TextField()
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

class d_originalmodel(models.Model):
    d_id = models.TextField(null=True)
    Business_id = models.TextField()
    seller_name = models.TextField()
    business_name = models.TextField()
    pan_number = models.TextField()
    gst = models.TextField()
    contact = models.TextField()
    alternate_contact = models.TextField()
    door_number = models.TextField(null=True)
    street_name = models.TextField(null=True)
    area = models.TextField(null=True)
    region = models.TextField(null=True)
    aadhar_number=models.TextField(null=True)
    pin_number = models.TextField()
    fssa = models.TextField()
    pin_your_location = models.TextField()
    name = models.TextField()
    account_number = models.TextField()
    ifsc_code = models.TextField()
    upi_id = models.TextField()
    gpay_number = models.TextField()
    aadhar = models.TextField()
    pan_file = models.TextField()
    profile = models.TextField()
    bank_passbook = models.TextField()
    gst_file = models.TextField()
    date=models.DateField(auto_now_add=True,null=True)
    category=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
    latitude = models.TextField(null=True)
    longitude = models.TextField(null=True)

# product models
# shop_products_categories
class shop_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    subcategory1 = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
   

# jewellery
class jewel_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    jewel_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)

# food
class food_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)

#freshcutsproductmodel

class fresh_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)

# dailymioproducts

class dmio_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)

#pharmacy products

class pharmacy_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)

# d_originalproducts
    
class d_original_productsmodel(models.Model):
    product_id = models.TextField(null=True)
    d_id = models.TextField(null=True)
    status = models.TextField(default=False,null=True)
    category = models.TextField(null=True)
    subcategory = models.TextField(null=True)
    product= models.JSONField(null=True)
    created_date=models.DateField(auto_now_add=True,null=True)
    district = models.TextField(null=True)



# ................# End_User Signin................
    
class End_Usermodel(models.Model):
    # User ID
    uid = models.TextField()
    # Signup
    email = models.EmailField()
    phone_number = models.TextField(null=True)
    password = models.TextField()
    full_name=models.TextField()
    created_date=models.TextField(null=True)
    otp = models.IntegerField(null=True)
    user_otp = models.IntegerField(null=True)
    profile_picture = models.TextField(null=True)
    address_data = models.JSONField(null=True)
    temp_address =  models.JSONField(null=True)


# -------------delivery person---------------------
# delivery signin
class Delivery_model(models.Model):
    uid = models.TextField(null=True)
    name = models.TextField(null=True)
    phone_number = models.TextField(null=True)
    wp_number = models.TextField(null=True)
    email = models.EmailField()
    aadhar_number = models.TextField(null=True)
    pan_number = models.TextField(null=True)
    driving_licensenum = models.TextField(null=True)
    profile_picture = models.TextField(null=True)
    bank_name = models.TextField(null=True)
    acc_number = models.TextField(null=True)
    name_asper_passbook = models.TextField(null=True)
    ifsc_code = models.TextField(null=True)
    bank_passbok_pic = models.TextField(null=True)
    aadhar_pic = models.TextField(null=True)
    pan_pic = models.TextField(null=True)
    drlicence_pic = models.TextField(null=True)
    delivery_type = models.TextField(null=True)
    approve_status = models.TextField(null=True)
    today_earnings = models.TextField(null=True)
    region = models.TextField(null=True)
    submit_issues = models.TextField(null=True)
    upload_issues = models.TextField(null=True)






# order table
class Product_Ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = datetime.date.today()
    total_amount = models.TextField(null=True)
    business = models.ForeignKey(Businessmodel,on_delete=models.CASCADE,null=True)
    end_user = models.ForeignKey(End_Usermodel,on_delete=models.CASCADE,null=True)
    # delivery = models.ForeignKey(Delivery_model,on_delete=models.CASCADE,null=True)
    shop_id= models.ForeignKey(shoppingmodel,on_delete=models.CASCADE,null=True)
    jewel_id=models.ForeignKey(jewellerymodel,on_delete=models.CASCADE,null=True)
    food_id=models.ForeignKey(foodmodel,on_delete=models.CASCADE,null=True)
    fresh_id=models.ForeignKey(freshcutsmodel,on_delete=models.CASCADE,null=True)
    d_id=models.ForeignKey(d_originalmodel,on_delete=models.CASCADE,null=True)
    dmio_id=models.ForeignKey(dailymio_model,on_delete=models.CASCADE,null=True)
    pharm_id=models.ForeignKey(pharmacy_model,on_delete=models.CASCADE,null=True)
    product_id= models.TextField(null=True)
    shop_product = models.ForeignKey(shop_productsmodel,on_delete=models.CASCADE,null=True)
    food_product = models.ForeignKey(food_productsmodel,on_delete=models.CASCADE,null=True)
    jewel_product = models.ForeignKey(jewel_productsmodel,on_delete=models.CASCADE,null=True)
    dmio_product = models.ForeignKey(dmio_productsmodel,on_delete=models.CASCADE,null=True)
    pharmacy_product = models.ForeignKey(pharmacy_productsmodel,on_delete=models.CASCADE,null=True)
    d_original_product = models.ForeignKey(d_original_productsmodel,on_delete=models.CASCADE,null=True)
    freshcut_product = models.ForeignKey(fresh_productsmodel,on_delete=models.CASCADE,null=True)
    status = models.TextField(null=True)
    expDate= order_date + datetime.timedelta(days=7)
    expected_deliverydate=models.DateField(default=expDate,null=True)   
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    delivery_type= models.TextField(null=True)
    category_data = models.TextField(null=True)
    payment_type = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)




class Carts(models.Model):
    shop_product=models.ForeignKey(shop_productsmodel,on_delete=models.CASCADE)
    jewel_product=models.ForeignKey(jewel_productsmodel,on_delete=models.CASCADE)
    d_origin_product=models.ForeignKey(d_original_productsmodel,on_delete=models.CASCADE)
    dailymio_product=models.ForeignKey(dmio_productsmodel,on_delete=models.CASCADE)
    pharmacy_product=models.ForeignKey(pharmacy_productsmodel,on_delete=models.CASCADE)
    food_product=models.ForeignKey(food_productsmodel,on_delete=models.CASCADE)
    freshcut_product=models.ForeignKey(fresh_productsmodel,on_delete=models.CASCADE)
    user=models.ForeignKey(End_Usermodel,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)

    qty=models.PositiveIntegerField(default=1)




class Reviews(models.Model):
    user=models.ForeignKey(End_Usermodel,on_delete=models.CASCADE)
    shop_product=models.ForeignKey(shop_productsmodel,on_delete=models.CASCADE)
    jewel_product=models.ForeignKey(jewel_productsmodel,on_delete=models.CASCADE)
    d_origin_product=models.ForeignKey(d_original_productsmodel,on_delete=models.CASCADE)
    dailymio_product=models.ForeignKey(dmio_productsmodel,on_delete=models.CASCADE)
    pharmacy_product=models.ForeignKey(pharmacy_productsmodel,on_delete=models.CASCADE)
    food_product=models.ForeignKey(food_productsmodel,on_delete=models.CASCADE)
    freshcut_product=models.ForeignKey(fresh_productsmodel,on_delete=models.CASCADE)
    comment=models.CharField(max_length=240)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return self.comment



class Offers(models.Model):
    shop_product=models.ForeignKey(shop_productsmodel,on_delete=models.CASCADE)
    jewel_product=models.ForeignKey(jewel_productsmodel,on_delete=models.CASCADE)
    d_origin_product=models.ForeignKey(d_original_productsmodel,on_delete=models.CASCADE)
    dailymio_product=models.ForeignKey(dmio_productsmodel,on_delete=models.CASCADE)
    pharmacy_product=models.ForeignKey(pharmacy_productsmodel,on_delete=models.CASCADE)
    food_product=models.ForeignKey(food_productsmodel,on_delete=models.CASCADE)
    freshcut_product=models.ForeignKey(fresh_productsmodel,on_delete=models.CASCADE)

    discount=models.TextField(default=0)
    isAvailable=models.BooleanField(default=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)



