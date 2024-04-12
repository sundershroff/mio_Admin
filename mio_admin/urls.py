"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from mio_admin import views

urlpatterns = [
    path('admin_index/',views.index),
    path('admin_dashboard/',views.dashboard),
    path('admin_product_details/',views.product_details),
    path('admin_order_details/',views.order_details),
    path('admin_banner/',views.banner),
    path('admin_customer_service/',views.customer_service),
    path('admin_product_appaoval/',views.product_appaoval),
    path('admin_hub_details/',views.hub_details),
    path('admin_hub_menu1/',views.hub_menu1),
    path('admin_user_add/',views.user_add),
    path('admin_user_menu/',views.user_menu),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

