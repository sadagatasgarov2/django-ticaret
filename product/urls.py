from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment')
]