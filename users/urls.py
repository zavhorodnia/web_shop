from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('users/', views.users_view, name="users"),
    path('users/<int:user_id>/', views.UserDetails.as_view(), name="user_details"),
    path('users/<int:user_id>/edit/', views.edit_user, name="edit_user"),
    path('users/<int:user_id>/delete/', views.delete_user, name="delete_user"),
]
