from os import name

from django.urls import path

from order import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('addtocart/<int:id>', views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct', views.order_product, name='deletefromcart'),
]
