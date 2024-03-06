from django.db import models
from django.utils import timezone
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
    date=models.TextField()
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)

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
    date=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)


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
    date=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
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
    date=models.TextField()
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)

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
    date=models.TextField(null=True)
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
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
    date=models.TextField()
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
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
    date=models.TextField()
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
# product models
# shop_products_categories
class shop_electronicsmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
class shop_mobilemodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_furnituremodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_autoaccessoriesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_kitchenmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_fashionmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


class shop_appliancesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_groceriesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


class shop_petsuppliesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_toysmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_sportsmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_healthcaremodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_booksmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class shop_personalcaremodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

# jewellery
class jewel_goldmodel(models.Model):
    product_id = models.TextField(null=True)
    jewel_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class jewel_silvermodel(models.Model):
    product_id = models.TextField(null=True)
    jewel_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

# food

class food_tiffenmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_mealsmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_biriyanimodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_chickenbiriyanimodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


class food_beefmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_chinesemodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


class food_pizzamodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_teacoffemodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_icecreammodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_firedchickenmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_burgermodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_cakemodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class food_bakerymodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

#freshcutsproductmodel

class fresh_chickenmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_muttonmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_beefmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_fishseafoodmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


class fresh_dryfishmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_prawnsmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


class fresh_eggmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_pondfishmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_meatmasalamodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_combomodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class fresh_choppedvegmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


# dailymioproducts

class dmio_grocerymodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class dmio_meatmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class dmio_fishmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class dmio_eggsmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class dmio_fruitsmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class dmio_vegitablesmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class dmio_dairymodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)


#pharmacy products
    
class pharmacy_allopathicmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class pharmacy_ayurvedicmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class pharmacy_siddhamodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class pharmacy_unanimodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

class pharmacy_herbaldrinksmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)

# d_originalproducts
class d_originalproductsmodel(models.Model):
    product_id = models.TextField(null=True)
    d_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)



# orderModel
class shop_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    shop_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)    
    delivery_date = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)

class jewel_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    jewel_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)


class food_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    food_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)

class fresh_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    fresh_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)

class dorigin_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    d_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)

class daily_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    dmio_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)

class pharmacy_ordermodel(models.Model):
    order_id = models.TextField(null=True)
    track_id = models.TextField(null=True)
    quantity = models.TextField(null=True)
    order_date = models.DateField(auto_now_add=True,null=True)
    total_amount = models.TextField(null=True)
    business_id = models.TextField(null=True)
    pharm_id= models.TextField(null=True)
    product_id = models.TextField(null=True)
    e_user_id = models.TextField(null=True)
    status = models.TextField(null=True)


# End_User Signin
class End_Usermodel(models.Model):
    # User ID
    uid = models.TextField()
    # Signup
    email = models.EmailField()
    phone_number = models.TextField(null=True)
    password = models.TextField()
    full_name=models.TextField()
    created_date=models.TextField(null=True)