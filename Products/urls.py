from django.contrib import admin
from django.urls import path,include
from .views import Products,StockTransactionView
from . import views

urlpatterns = [
   path('',Products,name='product'),
   path('transactions/', StockTransactionView.as_view(), name='stock_transactions'),

   # path('products/<int:product_id>/', views.ProductDetail, name='product_detail'),

]