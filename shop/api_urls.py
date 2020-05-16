from django.urls import path
from . import api_views as views

urlpatterns = [
    path('shops/', views.Shops.as_view(), name="api_shops"),
    path('shops/<int:shop_id>/', views.ShopDetail.as_view(), name="api_shop_details"),
]