from django.urls import path

from user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('orders/', views.orders, name='orders'),
    path('orderdetail/<int:id>', views.order_detail, name='order_detail'),
    path('comments/', views.comments, name='comments'),
    path('contents/', views.contents, name='contents'),
    path('addcontent/', views.addcontent, name='addcontent'),
    path('editcontent/<int:id>', views.editcontent, name='editcontent'),
    path('deletecontent/<int:id>', views.deletecontent, name='deletecontent')

]
