from django.contrib import admin
from django.urls import path,include
from .views import CustomerView
from . import views

urlpatterns = [
   # path('',CustomerView.as_view(),name='customer'),
   
      # path('products/<int:product_id>/', views.ProductDetail, name='product_detail'),


]