from django.urls import path
from . import views


urlpatterns = [
    path('shops/', views.shops_view, name="shops"),
    path('shops/add/', views.create_shop, name="create_shop"),
    path('shops/<int:shop_id>/', views.shop_details, name="shop_details"),
    path('shops/<int:shop_id>/edit/', views.edit_shop, name="edit_shop"),
    path('shops/<int:shop_id>/delete/', views.delete_shop, name="delete_shop"),
]