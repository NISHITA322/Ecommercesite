"""eVitalRX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from Ecomerce_Site.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home, navigation bar and about page
    path('',home,name="home"),
    path('navbar/', navbar, name="navbar"),
    path('about/',about,name="about"),

    # Admin setup (login-home and dashboard)
    path('admin_login/', adminLogin, name="admin_login"),
    path('adminhome/', adminHome, name="adminhome"),
    path('admin_dashboard/', admin_dashboard, name="admin_dashboard"),

    #  CRUD operation on category
    path('add_category/', add_category, name="add_category"),
    path('view_category/', view_category, name="view_category"),
    path('delete_category/<int:pid>/', delete_category, name="delete_category"),

    # CRUD operation on product
    path('add_product/', add_product, name='add_product'),
    path('view_product/', view_product, name='view_product'),
    path('edit_product/<int:pid>/', edit_product, name="edit_product"),
    path('delete_product/<int:pid>/', delete_product, name="delete_product"),

    # user registration and login - logout
    path('signup/', signup, name="signup"),
    path('userlogin/', userlogin, name="userlogin"),
    path('logout/', logoutuser, name="logout"),

    # user visit products page and product details page
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),

    # User adds the product in cart, set the quantity
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),

    # book and track or cancel the order
    path('booking/', booking, name="booking"),
    path('my-order/', myOrder, name="myorder"),
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),

    # admin manages order
    path('manage-order/', manage_order, name="manage_order"), 
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 

    # admin views user and delete the user
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),

    # 4 queries
    path('query_1/',query_1,name="query_1/"),
    path('query3/',query3,name="query3"),
    path('query2/',query2,name='query2'),  
    path('orders_summary/',orders_summary,name='orders_summary'), # no 4

    # manually updates date~
    path('booking/<int:pk>/update/', update_booking, name='update_booking'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
