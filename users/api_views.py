from .models import ShopUser
from .serializers import UserSerializer, UserRegistrationSerializer
from rest_framework import generics, permissions
from .permissions import IsShopAdmin, IsShopAdminOrGetSelf
from rest_framework.views import APIView, Response, status


class UserSignup(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Users(generics.ListCreateAPIView):
    queryset = ShopUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsShopAdmin)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShopUser.objects.all()
    lookup_field = 'id'
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsShopAdminOrGetSelf)
