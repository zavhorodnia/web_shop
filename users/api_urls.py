from django.urls import path
from . import api_views as views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('signup/', views.UserSignup.as_view(), name="signup"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('users/', views.Users.as_view(), name="users"),
    path('users/<int:id>/', views.UserDetail.as_view(), name="user_details"),
]
