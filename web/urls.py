from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api import business_views
from api import end_user_views,delivery_views
from web import end_usersview
from django.urls import path, include
from mio_admin import views
urlpatterns = [

# ..............enduser_web................

    path('enduser/usersignup',end_usersview.usersignup),
    path('enduser/usersignin',end_usersview.usersignin),
    path('enduser/end_user_otp/<id>',end_usersview.otp),
    path('enduser/profile_picture/<id>',end_usersview.profile_picture),
    path('enduser/dashboard/<id>',end_usersview.dashboard),

    path("shopproducts/shop/",end_usersview.shop), 
    path("shopproducts/shop_products/<str:category>",end_usersview.shop_products),
    path("shopproducts/single_products/<id>/<product_id>",end_usersview.single_shopproducts),
    path('shopproduct_categorywise/<id>/<str:category>/',end_usersview.shopproduct_category),
    path('singleproduct/enduser/<id>/<shop_id>/<product_id>',end_usersview.user_single_products),
    
    path("foodproducts/food",end_usersview.food),
    path('food_products/<str:category>',end_usersview.food_products),
    path('food_products/single_food/<id>/<product_id>/',end_usersview.single_food_products),
    path("foodproducts/food/<id>",end_usersview.user_foodpage),
    path('food_products_category/<id>/<str:category>',end_usersview.food_products_category), 
    path('food_products/single_food/<id>/<shop_id><product_id>/',end_usersview.user_singlefood_products),

    path("freshproducts/fresh_cuts",end_usersview.fresh_cuts),
    path("freshproducts/fresh_cuts/category/<str:category>/",end_usersview.fresh_cut_products),
    path("freshproducts/fresh_single_product/<id>/<product_id>",end_usersview.fresh_cut_singel_products),
    path("freshproducts/fresh_cuts/<id>",end_usersview.user_fresh_cuts),
    path("freshproducts/fresh_cuts_category/<id>/<str:category>/",end_usersview.user_freshcut_products),
    path("freshproducts/single_product/<id>/<shop_id>/<product_id>",end_usersview.user_freshcut_single_products),

    path("doriginalproducts/doriginal",end_usersview.doriginal),
    path("doriginalproducts/doriginal/<id>/<product_id>",end_usersview.d_original_single_products),
    path("doriginalproducts/doriginal/<id>",end_usersview.user_doriginal),
    path("doriginalproducts/doriginal/<id>/<shop_id>/<product_id>",end_usersview.user_doriginal_single_products),

    path("dailymioproducts/daily_mio",end_usersview.daily_mio),
    path("dailymioproducts/daily_mio/category/<str:category>/",end_usersview.daily_mio_products),
    path("dailymioproducts/dmio_singleproduct/<id>/<product_id>",end_usersview.daily_mio_single_products),
    path("dailymioproducts/daily_mio/<id>",end_usersview.user_daily_mio),
    path("dailymioproducts/daily_mio/<id>/<str:category>/",end_usersview.user_dmio_products),
    path("dailymioproducts/dmio_singleproduct/<id>/<shop_id>/<product_id>",end_usersview.user_dailymio_single_products),

    path("jewelleryproducts/jewellery/",end_usersview.jewellery),
    path("jewelleryproducts/jewellery/<str:category>",end_usersview.jewellery_products),
    path("jewelleryproducts/jewellery/<id>/<product_id>",end_usersview.jewellery_single_products),
    path("jewelleryproducts/jewellery/<id>",end_usersview.user_jewellery),
    path("jewelleryproducts/jewellery/<id>/<str:category>",end_usersview.user_jewellery_products),
    path("jewelleryproducts/jewellery/<id>/<shop_id>/<product_id>",end_usersview.user_jewel_single_product),

    path("pharmacyproducts/pharmacy/",end_usersview.pharmacy),
    path("pharmacyproducts/pharmacy/<str:category>",end_usersview.pharmac_products),
    path("pharmacyproducts/pharmacy_single/<id>/<product_id>",end_usersview.pharmac_single_products),
    path("pharmacyproducts/pharmacy/<id>",end_usersview.user_pharmacy),
    path("pharmacyproducts/pharmacy/<id>/<str:category>",end_usersview.user_pharm_products),
    path("pharmacyproducts/pharmacy_single/<id>/<shop_id>/<product_id>",end_usersview.user_pharmac_singleproduct),

    path("shopproducts/shopping_checkout",end_usersview.shopping_checkout),
    path('shopproducts/order/',end_usersview.order),
    path("shopproducts/shopping_cart",end_usersview.shopping_cart),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
