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
    hub = models.TextField(null=True)
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
    hub = models.TextField(null=True)
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
    hub = models.TextField(null=True)
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
    date=models.TextField()
    total_revenue = models.TextField(null=True)
    monthly_revenue = models.TextField(null=True)
# product models
# shop_products_categories
class shop_electronicsmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    elect = models.TextField(null=True)
class shop_mobilemodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    mob = models.TextField(null=True)
class shop_furnituremodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    fur = models.TextField(null=True)

class shop_autoaccessoriesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    auto = models.TextField(null=True)

class shop_kitchenmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    kit = models.TextField(null=True)

class shop_fashionmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    fas = models.TextField(null=True)

class shop_appliancesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    appl = models.TextField(null=True)

class shop_groceriesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    groc = models.TextField(null=True)


class shop_petsuppliesmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    pets = models.TextField(null=True)


class shop_toysmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    toys = models.TextField(null=True)
 

class shop_sportsmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    sport = models.TextField(null=True)


class shop_healthcaremodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    health = models.TextField(null=True)


class shop_booksmodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    book = models.TextField(null=True)


class shop_personalcaremodel(models.Model):
    product_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    pers = models.TextField(null=True)


# jewellery
class jewel_goldmodel(models.Model):
    product_id = models.TextField(null=True)
    jewel_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    gold = models.TextField(null=True)

class jewel_silvermodel(models.Model):
    product_id = models.TextField(null=True)
    jewel_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    silver = models.TextField(null=True)

# food

class food_tiffenmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    tiffen = models.TextField(null=True)

class food_mealsmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    meals = models.TextField(null=True)

class food_biriyanimodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    biriyani = models.TextField(null=True)

class food_chickenbiriyanimodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    chicken = models.TextField(null=True)

class food_beefmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    beef = models.TextField(null=True)



class food_chinesemodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    chinese = models.TextField(null=True)

class food_pizzamodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    pizza = models.TextField(null=True)

class food_teacoffemodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    tea = models.TextField(null=True)

class food_icecreammodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    icecream = models.TextField(null=True)

class food_firedchickenmodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    fired = models.TextField(null=True)


class food_burgermodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    burger = models.TextField(null=True)

class food_cakemodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    cake = models.TextField(null=True)

class food_bakerymodel(models.Model):
    product_id = models.TextField(null=True)
    food_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    bakery = models.TextField(null=True)

#freshcutsproductmodel

class fresh_chickenmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    chicken = models.TextField(null=True)

class fresh_muttonmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    mutton = models.TextField(null=True)

class fresh_beefmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    beef = models.TextField(null=True)

class fresh_fishseafoodmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    fish = models.TextField(null=True)


class fresh_dryfishmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    dry = models.TextField(null=True)

class fresh_prawnsmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    prawns = models.TextField(null=True)

class fresh_eggmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    egg = models.TextField(null=True)

class fresh_pondfishmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    pond = models.TextField(null=True)

class fresh_meatmasalamodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    meat = models.TextField(null=True)

class fresh_combomodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    combo = models.TextField(null=True)

class fresh_choppedvegmodel(models.Model):
    product_id = models.TextField(null=True)
    fresh_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    chopp = models.TextField(null=True)


# dailymioproducts

class dmio_grocerymodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    grocery = models.TextField(null=True)

class dmio_meatmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    meat = models.TextField(null=True)

class dmio_fishmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    fish = models.TextField(null=True)

class dmio_eggsmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    eggs = models.TextField(null=True)

class dmio_fruitsmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    fruits = models.TextField(null=True)

class dmio_vegitablesmodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    veg = models.TextField(null=True)

class dmio_dairymodel(models.Model):
    product_id = models.TextField(null=True)
    dmio_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    dairy = models.TextField(null=True)


#pharmacy products
    
class pharmacy_allopathicmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    allo = models.TextField(null=True)

class pharmacy_ayurvedicmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    ayur = models.TextField(null=True)

class pharmacy_siddhamodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    siddha = models.TextField(null=True)

class pharmacy_unanimodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    unani = models.TextField(null=True)

class pharmacy_herbaldrinksmodel(models.Model):
    product_id = models.TextField(null=True)
    pharm_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    herbal = models.TextField(null=True)

# d_originalproducts
class d_originalproductsmodel(models.Model):
    product_id = models.TextField(null=True)
    d_id = models.TextField(null=True)
    status = models.BooleanField(default=False,null=True)
    d_original = models.TextField(null=True)


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
    payment_status = models.TextField(null=True)
    
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
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)

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
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)
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
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)

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
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)

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
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)
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
    delivery_date = models.DateField(null=True)
    payment_status = models.TextField(null=True)
    def save(self, *args, **kwargs):
        if self.status == 'delivered' and not self.delivery_date:
            self.delivery_date = timezone.now().date()
        super().save(*args, **kwargs)

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
    otp = models.IntegerField(null=True)
    user_otp = models.IntegerField(null=True)
    profile_picture = models.TextField(null=True)



# -------------delivery person---------------------
# delivery signin
class Delivery_model(models.Model):
    uid = models.TextField()
    email = models.EmailField()
    phone_number = models.TextField(null=True)
    password = models.TextField()
    full_name=models.TextField()
    created_date=models.TextField(null=True)
    otp = models.IntegerField(null=True)
    user_otp = models.IntegerField(null=True)
    profile_picture = models.TextField(null=True)


