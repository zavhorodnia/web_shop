from django.urls import path
from . import api_views as views

urlpatterns = [
    path('shops/', views.Shops.as_view(), name="shops"),
    path('shops/<int:shop_id>/', views.ShopDetail.as_view(), name="shop_details"),
]