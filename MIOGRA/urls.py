"""
URL configuration for MIOGRA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api import business_views
from api import end_user_views,delivery_views
from web import end_usersview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('business_signup/',business_views.business_signup),
    path('business_otp/<id>',business_views.business_otp),
    path('business_signin/',business_views.business_signin),
    path('my_accounts_data/<id>',business_views.my_accounts_data),
    path('forget_password/',business_views.forget_password),
    path('resend_otp/<id>',business_views.resend_otp),
    path('business_profile_picture/<id>',business_views.business_profile_picture),
    

    # shopping
    path('shopping/<id>',business_views.shopping),
    path('shopping_alldata',business_views.shopping_alldata),
    path('my_shopping_data/<id>',business_views.my_shopping_data),
    path('shopping_update/<id>/shops/<shop_id>',business_views.shopping_update),
    path('business_shopping_data/<id>',business_views.business_shopping_data),

    # shopping dashboard
    path('shop_total_revenue/<id>',business_views.shop_total_revenue),
    path('shop_mon_revenue/<id>',business_views.shop_mon_revenue),
    path('shop_orderstatus/<id>',business_views.shop_orderstatus),
    path('shop_all_products/<id>',business_views.shop_all_products),
    path('product_status_cancel/<id>',business_views.product_status_cancel),
    path('product_status_delivered/<id>',business_views.product_status_delivered),
    path('product_status_on_process/<id>',business_views.product_status_on_process),
    path('shopproducts_orderhistory/<id>',business_views.shopproducts_orderhistory),
    # shop_product electronics
    path('shop_electronics/<id>',business_views.shop_electronics),
    path('shop_get_electronics/<id>',business_views.shop_get_electronics),
    path('shop_get_my_electronics/<id>/product/<product_id>',business_views.shop_get_my_electronics),
    path('shop_delete_electronics/<id>/product/<product_id>',business_views.shop_delete_electronics),
    path('shop_update_electronics/<id>/product/<product_id>',business_views.shop_update_electronics),
    path('shop_get_adminelectronics',business_views.shop_get_adminelectronics),
    path('electorder_date/<id>',business_views.electorder_date),


    # shop_product mobile
    path('shop_mobile/<id>',business_views.shop_mobile),
    path('shop_get_mobile/<id>',business_views.shop_get_mobile),
    path('shop_get_my_mobile/<id>/product/<product_id>',business_views.shop_get_my_mobile),
    path('shop_delete_mobile/<id>/product/<product_id>',business_views.shop_delete_mobile),
    path('shop_update_mobile/<id>/product/<product_id>',business_views.shop_update_mobile),
    path('shop_get_adminmobile',business_views.shop_get_adminmobile),
    path('mobileorder_date/<id>',business_views.mobileorder_date),

    # shop_product furniture
    path('shop_furniture/<id>',business_views.shop_furniture),
    path('shop_get_furniture/<id>',business_views.shop_get_furniture),
    path('shop_get_my_furniture/<id>/product/<product_id>',business_views.shop_get_my_furniture),
    path('shop_delete_furniture/<id>/product/<product_id>',business_views.shop_delete_furniture),
    path('shop_update_furniture/<id>/product/<product_id>',business_views.shop_update_furniture),
    path('shop_get_adminfurniture',business_views.shop_get_adminfurniture),
    path('furnitureorder_date/<id>',business_views.furnitureorder_date),

    # shop_product autoaccessories
    path('shop_autoaccessories/<id>',business_views.shop_autoaccessories),
    path('shop_get_autoaccessories/<id>',business_views.shop_get_autoaccessories),
    path('shop_get_my_autoaccessories/<id>/product/<product_id>',business_views.shop_get_my_autoaccessories),
    path('shop_delete_autoaccessories/<id>/product/<product_id>',business_views.shop_delete_autoaccessories),
    path('shop_update_autoaccessories/<id>/product/<product_id>',business_views.shop_update_autoaccessories),
    path('shop_get_adminautoaccessories',business_views.shop_get_adminautoaccessories),
    path('mobileorder_date/<id>',business_views.mobileorder_date),

    # shop_product kitchen
    path('shop_kitchen/<id>',business_views.shop_kitchen),
    path('shop_get_kitchen/<id>',business_views.shop_get_kitchen),
    path('shop_get_my_kitchen/<id>/product/<product_id>',business_views.shop_get_my_kitchen),
    path('shop_delete_kitchen/<id>/product/<product_id>',business_views.shop_delete_kitchen),
    path('shop_update_kitchen/<id>/product/<product_id>',business_views.shop_update_kitchen),
    path('shop_get_adminkitchen',business_views.shop_get_adminkitchen),
    path('kitchenorder_date/<id>',business_views.kitchenorder_date),

    # shop_product fashion
    path('shop_fashion/<id>',business_views.shop_fashion),
    path('shop_get_fashion/<id>',business_views.shop_get_fashion),    
    path('shop_get_my_fashion/<id>/product/<product_id>',business_views.shop_get_my_fashion),
    path('shop_delete_fashion/<id>/product/<product_id>',business_views.shop_delete_fashion),
    path('shop_update_fashion/<id>/product/<product_id>',business_views.shop_update_fashion),
    path('shop_get_adminfashion',business_views.shop_get_adminfashion),
    path('fashionorder_date/<id>',business_views.fashionorder_date),

    # shop_product appliances
    path('shop_appliances/<id>',business_views.shop_appliances),
    path('shop_get_appliances/<id>',business_views.shop_get_appliances),
    path('shop_get_my_appliances/<id>/product/<product_id>',business_views.shop_get_my_appliances),
    path('shop_delete_appliances/<id>/product/<product_id>',business_views.shop_delete_appliances),
    path('shop_update_appliances/<id>/product/<product_id>',business_views.shop_update_appliances),
    path('shop_get_adminappliances',business_views.shop_get_adminappliances),
    path('appliancesorder_date/<id>',business_views.appliancesorder_date),

    # shop_product groceries
    path('shop_groceries/<id>',business_views.shop_groceries),
    path('shop_get_groceries/<id>',business_views.shop_get_groceries),
    path('shop_get_my_groceries/<id>/product/<product_id>',business_views.shop_get_my_groceries),
    path('shop_delete_groceries/<id>/product/<product_id>',business_views.shop_delete_groceries),
    path('shop_update_groceries/<id>/product/<product_id>',business_views.shop_update_groceries),
    path('shop_get_admingroceries',business_views.shop_get_admingroceries),
    path('groceriesorder_date/<id>',business_views.groceriesorder_date),

    # shop_product petsupplies
    path('shop_petsupplies/<id>',business_views.shop_petsupplies),
    path('shop_get_petsupplies/<id>',business_views.shop_get_petsupplies),
    path('shop_get_my_petsupplies/<id>/product/<product_id>',business_views.shop_get_my_petsupplies),
    path('shop_delete_petsupplies/<id>/product/<product_id>',business_views.shop_delete_petsupplies),
    path('shop_update_petsupplies/<id>/product/<product_id>',business_views.shop_update_petsupplies),
    path('shop_get_adminpetsupplies',business_views.shop_get_adminpetsupplies),
    path('petsuppliesorder_date/<id>',business_views.petsuppliesorder_date),

    # shop_product toys
    path('shop_toys/<id>',business_views.shop_toys),
    path('shop_get_toys/<id>',business_views.shop_get_toys),
    path('shop_get_my_toys/<id>/product/<product_id>',business_views.shop_get_my_toys),
    path('shop_delete_toys/<id>/product/<product_id>',business_views.shop_delete_toys),
    path('shop_update_toys/<id>/product/<product_id>',business_views.shop_update_toys),
    path('shop_get_admintoys',business_views.shop_get_admintoys),
    path('toysorder_date/<id>',business_views.toysorder_date),

    # shop_product sports
    path('shop_sports/<id>',business_views.shop_sports),
    path('shop_get_sports/<id>',business_views.shop_get_sports),
    path('shop_get_my_sports/<id>/product/<product_id>',business_views.shop_get_my_sports),
    path('shop_delete_sports/<id>/product/<product_id>',business_views.shop_delete_sports),
    path('shop_update_sports/<id>/product/<product_id>',business_views.shop_update_sports),
    path('shop_get_adminsports',business_views.shop_get_adminsports),
    path('sportsorder_date/<id>',business_views.sportsorder_date),

    # shop_product healthcare
    path('shop_healthcare/<id>',business_views.shop_healthcare),
    path('shop_get_healthcare/<id>',business_views.shop_get_healthcare),
    path('shop_get_my_healthcare/<id>/product/<product_id>',business_views.shop_get_my_healthcare),
    path('shop_delete_healthcare/<id>/product/<product_id>',business_views.shop_delete_healthcare),
    path('shop_update_healthcare/<id>/product/<product_id>',business_views.shop_update_healthcare),
    path('shop_get_adminhealthcare',business_views.shop_get_adminhealthcare),
    path('healthcareorder_date/<id>',business_views.healthcareorder_date),

    # shop_product books
    path('shop_books/<id>',business_views.shop_books),
    path('shop_get_books/<id>',business_views.shop_get_books),
    path('shop_get_my_books/<id>/product/<product_id>',business_views.shop_get_my_books),
    path('shop_delete_books/<id>/product/<product_id>',business_views.shop_delete_books),
    path('shop_update_books/<id>/product/<product_id>',business_views.shop_update_books),
    path('shop_get_adminbooks',business_views.shop_get_adminbooks),
    path('booksorder_date/<id>',business_views.booksorder_date),


    # shop_product personalcare
    path('shop_personalcare/<id>',business_views.shop_personalcare),
    path('shop_get_personalcare/<id>',business_views.shop_get_personalcare),
    path('shop_get_my_personalcare/<id>/product/<product_id>',business_views.shop_get_my_personalcare),
    path('shop_delete_personalcare/<id>/product/<product_id>',business_views.shop_delete_personalcare),
    path('shop_update_personalcare/<id>/product/<product_id>',business_views.shop_update_personalcare),
    path('shop_get_adminpersonalcare',business_views.shop_get_adminpersonalcare),
    path('personalcareorder_date/<id>',business_views.personalcareorder_date),







# jewellery
    path('jewellery/<id>',business_views.jewellery),
    path('jewellery_alldata',business_views.jewellery_alldata),
    path('my_jewellery_data/<id>',business_views. my_jewellery_data),
    path('jewellery_update/<id>/jewels/<jewel_id>',business_views.jewellery_update),
    path('business_jewellery_data/<id>',business_views.business_jewellery_data),
    
    # dashboard

    path('jewel_total_revenue/<id>',business_views.jewel_total_revenue),
    path('jewel_mon_revenue/<id>',business_views.jewel_mon_revenue),
    path('jewel_orderstatus/<id>',business_views.jewel_orderstatus),
    path('jewelproduct_status_cancel/<id>',business_views.jewelproduct_status_cancel),
    path('jewelproduct_status_on_process/<id>',business_views.jewelproduct_status_on_process),
    path('jewelproduct_status_delivered/<id>',business_views.jewelproduct_status_delivered),
    path('jewel_all_products/<id>',business_views.jewel_all_products),
    path('jewelproducts_orderhistory/<id>',business_views.jewelproducts_orderhistory),



    # jewellery_product gold
    path('jewel_gold/<id>',business_views.jewel_gold),
    path('jewel_get_gold/<id>',business_views.jewel_get_gold),
    path('jewel_get_my_gold/<id>/product/<product_id>',business_views.jewel_get_my_gold),
    path('jewel_delete_gold/<id>/product/<product_id>',business_views.jewel_delete_gold),
    path('jewel_update_gold/<id>/product/<product_id>',business_views.jewel_update_gold),
    path('jewel_get_admingold',business_views.jewel_get_admingold),
    path('goldorder_date/<id>',business_views.goldorder_date),

    
    # jewellery_product silver
    path('jewel_silver/<id>',business_views.jewel_gold),
    path('jewel_get_silver/<id>',business_views.jewel_get_silver),
    path('jewel_get_my_silver/<id>/product/<product_id>',business_views.jewel_get_my_silver),
    path('jewel_delete_silver/<id>/product/<product_id>',business_views.jewel_delete_silver),
    path('jewel_update_silver/<id>/product/<product_id>',business_views.jewel_update_silver),
    path('jewel_get_adminsilver',business_views.jewel_get_adminsilver),
    path('silverorder_date/<id>',business_views.silverorder_date),

    # food
    path('food/<id>',business_views.food),
    path('food_alldata',business_views.food_alldata),
    path('my_food_data/<id>',business_views. my_food_data),
    path('food_update/<id>/foods/<food_id>',business_views.food_update),
    path('business_food_data/<id>',business_views.business_food_data),
   
    # dashboard

    path('food_total_revenue/<id>',business_views.food_total_revenue),
    path('food_mon_revenue/<id>',business_views.food_mon_revenue),
    path('food_orderstatus/<id>',business_views.food_orderstatus),
    path('foodproduct_status_cancel/<id>',business_views.foodproduct_status_cancel),
    path('foodproduct_status_on_process/<id>',business_views.foodproduct_status_on_process),
    path('foodproduct_status_delivered/<id>',business_views.foodproduct_status_delivered),
    path('food_all_products/<id>',business_views.food_all_products),
    path('foodproducts_orderhistory/<id>',business_views.foodproducts_orderhistory),

    # food_product tiffen
    path('food_tiffen/<id>',business_views.food_tiffen),
    path('food_get_tiffen/<id>',business_views.food_get_tiffen),
    path('food_get_my_tiffen/<id>/product/<product_id>',business_views.food_get_my_tiffen),
    path('food_delete_tiffen/<id>/product/<product_id>',business_views.food_delete_tiffen),
    path('food_update_tiffen/<id>/product/<product_id>',business_views.food_update_tiffen),
    path('food_get_admintiffen',business_views.food_get_admintiffen),
    path('tiffenorder_date/<id>',business_views.tiffenorder_date),

    # food_product meals
    path('food_meals/<id>',business_views.food_meals),
    path('food_get_meals/<id>',business_views.food_get_meals),
    path('food_get_my_meals/<id>/product/<product_id>',business_views.food_get_my_meals),
    path('food_delete_meals/<id>/product/<product_id>',business_views.food_delete_meals),
    path('food_update_meals/<id>/product/<product_id>',business_views.food_update_meals),
    path('food_get_adminmeals',business_views.food_get_adminmeals),
    path('mealsorder_date/<id>',business_views.mealsorder_date),

    # food_product biriyani
    path('food_biriyani/<id>',business_views.food_biriyani),
    path('food_get_biriyani/<id>',business_views.food_get_biriyani),
    path('food_get_my_biriyani/<id>/product/<product_id>',business_views.food_get_my_biriyani),
    path('food_delete_biriyani/<id>/product/<product_id>',business_views.food_delete_biriyani),
    path('food_update_biriyani/<id>/product/<product_id>',business_views.food_update_biriyani),
    path('food_get_adminbiriyani',business_views.food_get_adminbiriyani),
    path('biriyaniorder_date/<id>',business_views.biriyaniorder_date),

    # food_product chickenbiriyani
    path('food_chickenbiriyani/<id>',business_views.food_chickenbiriyani),
    path('food_get_chickenbiriyani/<id>',business_views.food_get_chickenbiriyani),
    path('food_get_my_chickenbiriyani/<id>/product/<product_id>',business_views.food_get_my_chickenbiriyani),
    path('food_delete_chickenbiriyani/<id>/product/<product_id>',business_views.food_delete_chickenbiriyani),
    path('food_update_chickenbiriyani/<id>/product/<product_id>',business_views.food_update_chickenbiriyani),
    path('food_get_adminchickenbiriyani',business_views.food_get_adminchickenbiriyani),
    path('chickenbiriyaniorder_date/<id>',business_views.chickenbiriyaniorder_date),

    # food_product beef
    path('food_beef/<id>',business_views.food_beef),
    path('food_get_beef/<id>',business_views.food_get_beef),
    path('food_get_my_beef/<id>/product/<product_id>',business_views.food_get_my_beef),
    path('food_delete_beef/<id>/product/<product_id>',business_views.food_delete_beef),
    path('food_update_beef/<id>/product/<product_id>',business_views.food_update_beef),
    path('food_get_adminbeef',business_views.food_get_adminbeef),
    path('beeforder_date/<id>',business_views.beeforder_date),

    # food_product chinese
    path('food_chinese/<id>',business_views.food_chinese),
    path('food_get_chinese/<id>',business_views.food_get_chinese),
    path('food_get_my_chinese/<id>/product/<product_id>',business_views.food_get_my_chinese),
    path('food_delete_chinese/<id>/product/<product_id>',business_views.food_delete_chinese),
    path('food_update_chinese/<id>/product/<product_id>',business_views.food_update_chinese),
    path('food_get_adminchinese',business_views.food_get_adminchinese),
    path('chineseorder_date/<id>',business_views.chineseorder_date),

    # food_product pizza
    path('food_pizza/<id>',business_views.food_pizza),
    path('food_get_pizza/<id>',business_views.food_get_pizza),
    path('food_get_my_pizza/<id>/product/<product_id>',business_views.food_get_my_pizza),
    path('food_delete_pizza/<id>/product/<product_id>',business_views.food_delete_pizza),
    path('food_update_pizza/<id>/product/<product_id>',business_views.food_update_pizza),
    path('food_get_adminpizza',business_views.food_get_adminpizza),
    path('pizzaorder_date/<id>',business_views.pizzaorder_date),

    # food_product teacoffe
    path('food_teacoffe/<id>',business_views.food_teacoffe),
    path('food_get_teacoffe/<id>',business_views.food_get_teacoffe),
    path('food_get_my_teacoffe/<id>/product/<product_id>',business_views.food_get_my_teacoffe),
    path('food_delete_teacoffe/<id>/product/<product_id>',business_views.food_delete_teacoffe),
    path('food_update_teacoffe/<id>/product/<product_id>',business_views.food_update_teacoffe),
    path('food_get_adminteacoffe',business_views.food_get_adminteacoffe),
    path('teacoffeorder_date/<id>',business_views.teacoffeorder_date),


    # food_product icecream
    path('food_icecream/<id>',business_views.food_icecream),
    path('food_get_icecream/<id>',business_views.food_get_icecream),
    path('food_get_my_icecream/<id>/product/<product_id>',business_views.food_get_my_icecream),
    path('food_delete_icecream/<id>/product/<product_id>',business_views.food_delete_icecream),
    path('food_update_icecream/<id>/product/<product_id>',business_views.food_update_icecream),
    path('food_get_adminicecream',business_views.food_get_adminicecream),
    path('icecreamorder_date/<id>',business_views.icecreamorder_date),


    # food_product firedchicken
    path('food_firedchicken/<id>',business_views.food_firedchicken),
    path('food_get_firedchicken/<id>',business_views.food_get_firedchicken),
    path('food_get_my_firedchicken/<id>/product/<product_id>',business_views.food_get_my_firedchicken),
    path('food_delete_firedchicken/<id>/product/<product_id>',business_views.food_delete_firedchicken),
    path('food_update_firedchicken/<id>/product/<product_id>',business_views.food_update_firedchicken),
    path('food_get_adminfiredchicken',business_views.food_get_adminfiredchicken),
    path('firedchickenorder_date/<id>',business_views.firedchickenorder_date),


    # food_product burger
    path('food_burger/<id>',business_views.food_burger),
    path('food_get_burger/<id>',business_views.food_get_burger),
    path('food_get_my_burger/<id>/product/<product_id>',business_views.food_get_my_burger),
    path('food_delete_burger/<id>/product/<product_id>',business_views.food_delete_burger),
    path('food_update_burger/<id>/product/<product_id>',business_views.food_update_burger),
    path('food_get_adminburger',business_views.food_get_adminburger),
    path('burgerorder_date/<id>',business_views.burgerorder_date),

    # food_product cake
    path('food_cake/<id>',business_views.food_cake),
    path('food_get_cake/<id>',business_views.food_get_cake),
    path('food_get_my_cake/<id>/product/<product_id>',business_views.food_get_my_cake),
    path('food_delete_cake/<id>/product/<product_id>',business_views.food_delete_cake),
    path('food_update_cake/<id>/product/<product_id>',business_views.food_update_cake),
    path('food_get_admincake',business_views.food_get_admincake),
    path('cakeorder_date/<id>',business_views.cakeorder_date),

    # food_product bakery
    path('food_bakery/<id>',business_views.food_bakery),
    path('food_get_bakery/<id>',business_views.food_get_bakery),
    path('food_get_my_bakery/<id>/product/<product_id>',business_views.food_get_my_bakery),
    path('food_delete_bakery/<id>/product/<product_id>',business_views.food_delete_bakery),
    path('food_update_bakery/<id>/product/<product_id>',business_views.food_update_bakery),
    path('food_get_adminbakery',business_views.food_get_adminbakery),
    path('bakeryorder_date/<id>',business_views.bakeryorder_date),


    # freshcuts
    path('freshcuts/<id>',business_views.freshcuts),
    path('freshcuts_alldata',business_views.freshcuts_alldata),
    path('my_freshcuts_data/<id>',business_views. my_freshcuts_data),
    path('freshcuts_update/<id>/freshcuts/<fresh_id>',business_views.freshcuts_update),
    path('business_freshcuts_data/<id>',business_views.business_freshcuts_data),

    # dashboard
    path('fresh_total_revenue/<id>',business_views.fresh_total_revenue),
    path('fresh_mon_revenue/<id>',business_views.fresh_mon_revenue),
    path('fresh_orderstatus/<id>',business_views.fresh_orderstatus),
    path('freshproduct_status_cancel/<id>',business_views.freshproduct_status_cancel),
    path('freshproduct_status_on_process/<id>',business_views.freshproduct_status_on_process),
    path('freshproduct_status_delivered/<id>',business_views.freshproduct_status_delivered),
    path('fresh_all_products/<id>',business_views.fresh_all_products),
    path('freshproducts_orderhistory/<id>',business_views.freshproducts_orderhistory),


    # fresh_product chicken
    path('fresh_chicken/<id>',business_views.fresh_chicken),
    path('fresh_get_chicken/<id>',business_views.fresh_get_chicken),
    path('fresh_get_my_chicken/<id>/product/<product_id>',business_views.fresh_get_my_chicken),
    path('fresh_delete_chicken/<id>/product/<product_id>',business_views.fresh_delete_chicken),
    path('fresh_update_chicken/<id>/product/<product_id>',business_views.fresh_update_chicken),
    path('fresh_get_adminchicken',business_views.fresh_get_adminchicken),
    path('chickenorder_date/<id>',business_views.chickenorder_date),

    # fresh_product mutton
    path('fresh_mutton/<id>',business_views.fresh_mutton),
    path('fresh_get_mutton/<id>',business_views.fresh_get_mutton),
    path('fresh_get_my_mutton/<id>/product/<product_id>',business_views.fresh_get_my_mutton),
    path('fresh_delete_mutton/<id>/product/<product_id>',business_views.fresh_delete_mutton),
    path('fresh_update_mutton/<id>/product/<product_id>',business_views.fresh_update_mutton),
    path('fresh_get_adminmutton',business_views.fresh_get_adminmutton),
    path('muttonorder_date/<id>',business_views.muttonorder_date),

    # fresh_product beef
    path('fresh_beef/<id>',business_views.fresh_beef),
    path('fresh_get_beef/<id>',business_views.fresh_get_beef),
    path('fresh_get_my_beef/<id>/product/<product_id>',business_views.fresh_get_my_beef),
    path('fresh_delete_beef/<id>/product/<product_id>',business_views.fresh_delete_beef),
    path('fresh_update_beef/<id>/product/<product_id>',business_views.fresh_update_beef),
    path('fresh_get_adminbeef',business_views.fresh_get_adminbeef),
    path('beeforder_date/<id>',business_views.beeforder_date),

    # fresh_product fishseafood
    path('fresh_fishseafood/<id>',business_views.fresh_fishseafood),
    path('fresh_get_fishseafood/<id>',business_views.fresh_get_fishseafood),
    path('fresh_get_my_fishseafood/<id>/product/<product_id>',business_views.fresh_get_my_fishseafood),
    path('fresh_delete_fishseafood/<id>/product/<product_id>',business_views.fresh_delete_fishseafood),
    path('fresh_update_fishseafood/<id>/product/<product_id>',business_views.fresh_update_fishseafood),
    path('fresh_get_adminfishseafood',business_views.fresh_get_adminfishseafood),
    path('fishseafoodorder_date/<id>',business_views.fishseafoodorder_date),

    # fresh_productprawns
    path('fresh_prawns/<id>',business_views.fresh_prawns),
    path('fresh_get_prawns/<id>',business_views.fresh_get_prawns),
    path('fresh_get_my_prawns/<id>/product/<product_id>',business_views.fresh_get_my_prawns),
    path('fresh_delete_prawns/<id>/product/<product_id>',business_views.fresh_delete_prawns),
    path('fresh_update_prawns/<id>/product/<product_id>',business_views.fresh_update_prawns),
    path('fresh_get_adminprawns',business_views.fresh_get_adminprawns),
    path('prawnsorder_date/<id>',business_views.prawnsorder_date),

    # fresh_productegg
    path('fresh_egg/<id>',business_views.fresh_egg),
    path('fresh_get_egg/<id>',business_views.fresh_get_egg),
    path('fresh_get_my_egg/<id>/product/<product_id>',business_views.fresh_get_my_egg),
    path('fresh_delete_egg/<id>/product/<product_id>',business_views.fresh_delete_egg),
    path('fresh_update_egg/<id>/product/<product_id>',business_views.fresh_update_egg),
    path('fresh_get_adminegg',business_views.fresh_get_adminegg),
    path('eggorder_date/<id>',business_views.eggorder_date),

    # fresh_product pond
    path('fresh_pond/<id>',business_views.fresh_pond),
    path('fresh_get_pond/<id>',business_views.fresh_get_pond),
    path('fresh_get_my_pond/<id>/product/<product_id>',business_views.fresh_get_my_pond),
    path('fresh_delete_pond/<id>/product/<product_id>',business_views.fresh_delete_pond),
    path('fresh_update_pond/<id>/product/<product_id>',business_views.fresh_update_pond),
    path('fresh_get_adminpond',business_views.fresh_get_adminpond),
    path('pondorder_date/<id>',business_views.pondorder_date),

    # fresh_product meatmasala
    path('fresh_meatmasala/<id>',business_views.fresh_meatmasala),
    path('fresh_get_meatmasala/<id>',business_views.fresh_get_meatmasala),
    path('fresh_get_my_meatmasala/<id>/product/<product_id>',business_views.fresh_get_my_meatmasala),
    path('fresh_delete_meatmasala/<id>/product/<product_id>',business_views.fresh_delete_meatmasala),
    path('fresh_update_meatmasala/<id>/product/<product_id>',business_views.fresh_update_meatmasala),
    path('fresh_get_adminmeatmasala',business_views.fresh_get_adminmeatmasala),
    path('meatmasalaorder_date/<id>',business_views.meatmasalaorder_date),

    # fresh_productcombo
    path('fresh_combo/<id>',business_views.fresh_combo),
    path('fresh_get_combo/<id>',business_views.fresh_get_combo),
    path('fresh_get_my_combo/<id>/product/<product_id>',business_views.fresh_get_my_combo),
    path('fresh_delete_combo/<id>/product/<product_id>',business_views.fresh_delete_combo),
    path('fresh_update_combo/<id>/product/<product_id>',business_views.fresh_update_combo),
    path('fresh_get_admincombo',business_views.fresh_get_admincombo),
    path('comboorder_date/<id>',business_views.comboorder_date),

    # fresh_productchoppedveg
    path('fresh_choppedveg/<id>',business_views.fresh_choppedveg),
    path('fresh_get_choppedveg/<id>',business_views.fresh_get_choppedveg),
    path('fresh_get_my_choppedveg/<id>/product/<product_id>',business_views.fresh_get_my_choppedveg),
    path('fresh_delete_choppedveg/<id>/product/<product_id>',business_views.fresh_delete_choppedveg),
    path('fresh_update_choppedveg/<id>/product/<product_id>',business_views.fresh_update_choppedveg),
    path('fresh_get_adminchoppedveg',business_views.fresh_get_adminchoppedveg),
    path('choppedvegorder_date/<id>',business_views.choppedvegorder_date),


    # dailymio
    path('dailymio/<id>',business_views.dailymio),
    path('dailymio_alldata',business_views.dailymio_alldata),
    path('my_dailymio_data/<id>',business_views. my_dailymio_data),
    path('dailymio_update/<id>/dailymio/<dmio_id>',business_views.dailymio_update),
    path('business_dailymio_data/<id>',business_views.business_dailymio_data),

    # dashboard
    path('dmio_total_revenue/<id>',business_views.dmio_total_revenue),
    path('dmio_mon_revenue/<id>',business_views.dmio_mon_revenue),
    path('dmio_orderstatus/<id>',business_views.dmio_orderstatus),
    path('dmioproduct_status_cancel/<id>',business_views.dmioproduct_status_cancel),
    path('dmioproduct_status_on_process/<id>',business_views.dmioproduct_status_on_process),
    path('dmioproduct_status_delivered/<id>',business_views.dmioproduct_status_delivered),
    path('dmio_all_products/<id>',business_views.dmio_all_products),
    path('dmioproducts_orderhistory/<id>',business_views.dmioproducts_orderhistory),

    # dailymio_productgrocery 
    path('dmio_grocery/<id>',business_views.dmio_grocery),
    path('dmio_get_grocery/<id>',business_views.dmio_get_grocery),
    path('dmio_get_my_grocery/<id>/product/<product_id>',business_views.dmio_get_my_grocery),
    path('dmio_delete_grocery/<id>/product/<product_id>',business_views.dmio_delete_grocery),
    path('dmio_update_grocery/<id>/product/<product_id>',business_views.dmio_update_grocery),
    path('dmio_get_admingrocery',business_views.dmio_get_admingrocery),
    path('groceryorder_date/<id>',business_views.groceryorder_date),

    # dailymio_product meat
    path('dmio_meat/<id>',business_views.dmio_meat),
    path('dmio_get_meat/<id>',business_views.dmio_get_meat),
    path('dmio_get_my_meat/<id>/product/<product_id>',business_views.dmio_get_my_meat),
    path('dmio_delete_meat/<id>/product/<product_id>',business_views.dmio_delete_meat),
    path('dmio_update_meat/<id>/product/<product_id>',business_views.dmio_update_meat),
    path('dmio_get_adminmeat',business_views.dmio_get_adminmeat),
    path('meatorder_date/<id>',business_views.meatorder_date),

    # dailymio_product fish
    path('dmio_fish/<id>',business_views.dmio_fish),
    path('dmio_get_fish/<id>',business_views.dmio_get_fish),
    path('dmio_get_my_fish/<id>/product/<product_id>',business_views.dmio_get_my_fish),
    path('dmio_delete_fish/<id>/product/<product_id>',business_views.dmio_delete_fish),
    path('dmio_update_fish/<id>/product/<product_id>',business_views.dmio_update_fish),
    path('dmio_get_adminfish',business_views.dmio_get_adminfish),
    path('fishorder_date/<id>',business_views.fishorder_date),

    # dailymio_product eggs
    path('dmio_eggs/<id>',business_views.dmio_eggs),
    path('dmio_get_eggs/<id>',business_views.dmio_get_eggs),
    path('dmio_get_my_eggs/<id>/product/<product_id>',business_views.dmio_get_my_eggs),
    path('dmio_delete_eggs/<id>/product/<product_id>',business_views.dmio_delete_eggs),
    path('dmio_update_eggs/<id>/product/<product_id>',business_views.dmio_update_eggs),
    path('dmio_get_admineggs',business_views.dmio_get_admineggs),
    path('eggsorder_date/<id>',business_views.eggsorder_date),


    # dailymio_product fruits
    path('dmio_fruits/<id>',business_views.dmio_fruits),
    path('dmio_get_fruits/<id>',business_views.dmio_get_fruits),
    path('dmio_get_my_fruits/<id>/product/<product_id>',business_views.dmio_get_my_fruits),
    path('dmio_delete_fruits/<id>/product/<product_id>',business_views.dmio_delete_fruits),
    path('dmio_update_fruits/<id>/product/<product_id>',business_views.dmio_update_fruits),
    path('dmio_get_adminfruits',business_views.dmio_get_adminfruits),
    path('fruitsorder_date/<id>',business_views.fruitsorder_date),

    # dailymio_product vegitables
    path('dmio_evegitables/<id>',business_views.dmio_vegitables),
    path('dmio_get_vegitables/<id>',business_views.dmio_get_vegitables),
    path('dmio_get_my_vegitables/<id>/product/<product_id>',business_views.dmio_get_my_vegitables),
    path('dmio_delete_vegitables/<id>/product/<product_id>',business_views.dmio_delete_vegitables),
    path('dmio_update_vegitables/<id>/product/<product_id>',business_views.dmio_update_vegitables),
    path('dmio_get_adminvegitables',business_views.dmio_get_adminvegitables),
    path('vegitablesorder_date/<id>',business_views.vegitablesorder_date),


    # dailymio_product dairy
    path('dmio_dairy/<id>',business_views.dmio_dairy),
    path('dmio_get_dairy/<id>',business_views.dmio_get_dairy),
    path('dmio_get_my_dairy/<id>/product/<product_id>',business_views.dmio_get_my_dairy),
    path('dmio_delete_dairy/<id>/product/<product_id>',business_views.dmio_delete_dairy),
    path('dmio_update_dairy/<id>/product/<product_id>',business_views.dmio_update_dairy),
    path('dmio_get_admindairy',business_views.dmio_get_admindairy),
    path('dairyorder_date/<id>',business_views.dairyorder_date),

    
    # pharmacy
    path('pharmacy/<id>',business_views.pharmacy),
    path('pharmacy_alldata',business_views.pharmacy_alldata),
    path('my_pharmacy_data/<id>',business_views.my_pharmacy_data),
    path('pharmacy_update/<id>/pharmacy/<pharm_id>',business_views.pharmacy_update),
    path('business_pharmacy_data/<id>',business_views.business_pharmacy_data),

    # dashboard
    path('pharmacy_total_revenue/<id>',business_views.pharmacy_total_revenue),
    path('pharm_mon_revenue/<id>',business_views.pharm_mon_revenue),
    path('pharm_orderstatus/<id>',business_views.pharm_orderstatus),
    path('pharmproduct_status_cancel/<id>',business_views.pharmproduct_status_cancel),
    path('pharmproduct_status_on_process/<id>',business_views.pharmproduct_status_on_process),
    path('pharmproduct_status_delivered/<id>',business_views.pharmproduct_status_delivered),
    path('pharm_all_products/<id>',business_views.pharm_all_products),
    path('pharmacyproducts_orderhistory/<id>',business_views.pharmacyproducts_orderhistory),

    # pharmacy_ products allopathic
    path('pharmacy_allopathic/<id>',business_views.pharmacy_allopathic),
    path('pharmacy_get_allopathic/<id>',business_views.pharmacy_get_allopathic),
    path('pharmacy_get_my_allopathic/<id>/product/<product_id>',business_views.pharmacy_get_my_allopathic),
    path('pharmacy_delete_allopathic/<id>/product/<product_id>',business_views.pharmacy_delete_allopathic),
    path('pharmacy_update_allopathic/<id>/product/<product_id>',business_views.pharmacy_update_allopathic),
    path('pharmacy_get_adminallopathic',business_views.pharmacy_get_adminallopathic),
    path('allopathicorder_date/<id>',business_views.allopathicorder_date),

    # pharmacy_ products ayurvedic
    path('pharmacy_ayurvedic/<id>',business_views.pharmacy_ayurvedic),
    path('pharmacy_get_ayurvedic/<id>',business_views.pharmacy_get_ayurvedic),
    path('pharmacy_get_my_ayurvedic/<id>/product/<product_id>',business_views.pharmacy_get_my_ayurvedic),
    path('pharmacy_delete_ayurvedic/<id>/product/<product_id>',business_views.pharmacy_delete_ayurvedic),
    path('pharmacy_update_ayurvedic/<id>/product/<product_id>',business_views.pharmacy_update_ayurvedic),
    path('pharmacy_get_adminayurvedic',business_views.pharmacy_get_adminayurvedic),
    path('ayurvedicorder_date/<id>',business_views.ayurvedicorder_date),


    # pharmacy_ products siddha
    path('pharmacy_siddha/<id>',business_views.pharmacy_siddha),
    path('pharmacy_get_siddha/<id>',business_views.pharmacy_get_siddha),
    path('pharmacy_get_my_siddha/<id>/product/<product_id>',business_views.pharmacy_get_my_siddha),
    path('pharmacy_delete_siddha/<id>/product/<product_id>',business_views.pharmacy_delete_siddha),
    path('pharmacy_update_siddha/<id>/product/<product_id>',business_views.pharmacy_update_siddha),
    path('pharmacy_get_adminsiddha',business_views.pharmacy_get_adminsiddha),
    path('siddhaorder_date/<id>',business_views.siddhaorder_date),

    # pharmacy_ products unani
    path('pharmacy_unani/<id>',business_views.pharmacy_unani),
    path('pharmacy_get_unani/<id>',business_views.pharmacy_get_unani),
    path('pharmacy_get_my_unani/<id>/product/<product_id>',business_views.pharmacy_get_my_unani),
    path('pharmacy_delete_unani/<id>/product/<product_id>',business_views.pharmacy_delete_unani),
    path('pharmacy_update_unani/<id>/product/<product_id>',business_views.pharmacy_update_unani),
    path('pharmacy_get_adminunani',business_views.pharmacy_get_adminunani),
    path('unaniorder_date/<id>',business_views.unaniorder_date),

    # pharmacy_ products herbaldrinks
    path('pharmacy_herbaldrinks/<id>',business_views.pharmacy_herbaldrinks),
    path('pharmacy_get_herbaldrinks/<id>',business_views.pharmacy_get_herbaldrinks),
    path('pharmacy_get_my_herbaldrinks/<id>/product/<product_id>',business_views.pharmacy_get_my_herbaldrinks),
    path('pharmacy_delete_herbaldrinks/<id>/product/<product_id>',business_views.pharmacy_delete_herbaldrinks),
    path('pharmacy_update_herbaldrinks/<id>/product/<product_id>',business_views.pharmacy_update_herbaldrinks),
    path('pharmacy_get_adminherbaldrinks',business_views.pharmacy_get_adminherbaldrinks),
    path('herbaldrinksorder_date/<id>',business_views.herbaldrinksorder_date),

    # d_original
    path('d_original/<id>',business_views.d_original),
    path('d_original_alldata',business_views.d_original_alldata),
    path('my_d_original_data/<id>',business_views.my_d_original_data),
    path('d_original_update/<id>/d_original/<d_id>',business_views.d_original_update),
    path('business_d_original_data/<id>',business_views.business_d_original_data),

    # dashboard links

    path('d_origin_total_revenue/<id>',business_views.d_origin_total_revenue),
    path('d_origin_mon_revenue/<id>',business_views.d_origin_mon_revenue),
    path('d_origin_orderstatus/<id>',business_views.d_origin_orderstatus),
    path('d_origin_all_products/<id>',business_views.d_origin_all_products),
    path('d_originproduct_status_cancel/<id>',business_views.d_originproduct_status_cancel),
    path('d_originproduct_status_delivered/<id>',business_views.d_originproduct_status_delivered),
    path('d_originproduct_status_on_process/<id>',business_views.d_originproduct_status_on_process),
    path('d_originalproducts_orderhistory/<id>',business_views.d_originalproducts_orderhistory),

    # d_original_get_products
    path('d_original_product/<id>',business_views.d_original_product),
    path('d_original_get_product/<id>',business_views.d_original_get_product),
    path('d_original_get_my_product/<id>/product/<product_id>',business_views.d_original_get_my_product),
    path('d_original_delete_product/<id>/product/<product_id>',business_views.d_original_delete_product),
    path('d_original_update_product/<id>/product/<product_id>',business_views. d_original_update_product),
    path('d_original_get_adminproduct',business_views.d_original_get_adminproduct),
    path('productorder_date/<id>',business_views.productorder_date),





# ..............end_user........

    path('end_user_signup/',end_user_views.end_user_signup),
    path('end_user_signin/',end_user_views.end_user_signin),
    path('all_users_data/',end_user_views.all_users_data),
    path('end_user_otp/<id>',end_user_views.end_user_otp),
    path('endresend_otp/<id>',end_user_views.endresend_otp),
    path('endforget_password/',end_user_views.endforget_password),
    path('end_profile_picture/<id>',end_user_views.end_profile_picture),
    path('usershop_get_electronics/<id>',end_user_views.usershop_get_electronics),

# ..............enduser_web................

    path('enduser/usersignup',end_usersview.usersignup),
    path('enduser/usersignin',end_usersview.usersignin),
    path('enduser/end_user_otp/<id>',end_usersview.otp),
    path('enduser/profile_picture/<id>',end_usersview.profile_picture),
    path('enduser/dashboard/<id>',end_usersview.dashboard),
    path("shopproducts/shop/<id>",end_usersview.shop),

    path("foodproducts/food",end_usersview.food),
    path("freshproducts/fresh_cuts",end_usersview.fresh_cuts),
    path("doriginalproducts/doriginal",end_usersview.doriginal),
    path("dailymioproducts/daily_mio",end_usersview.daily_mio),
    path("jewelleryproducts/jewellery/<id>",end_usersview.jewellery),
    path("pharmacyproducts/pharmacy",end_usersview.pharmacy),


# .........................delivery...........................

    path('delivery_person_signup/',delivery_views.delivery_person_signup),
    path('delivery_person_signin/',delivery_views.delivery_person_signin),
    path('all_delivery_person_data/',delivery_views.all_delivery_person_data),
    path('delivery_person_otp/<id>',delivery_views.delivery_person_otp),
    path('deliveryresend_otp/<id>',delivery_views.deliveryresend_otp),
    path('delivery_forget_password/',delivery_views.delivery_forget_password),
    path('delivery_profile_picture/<id>',delivery_views.delivery_profile_picture),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

