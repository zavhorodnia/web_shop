from rest_framework import generics, permissions
from .models import Shop
from users.permissions import IsShopAdmin
from .serializers import ShopSerializer
from rest_framework.views import Response, status


class Shops(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = (permissions.IsAuthenticated, IsShopAdmin)

    def post(self, request):
        try:
            shop = Shop.objects.create(**request.data)
        except TypeError:
            return Response({'error': 'invalid format'}, status=status.HTTP_400_BAD_REQUEST)
        shop.users.set([request.user])
        serializer = self.serializer_class(shop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ShopDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    lookup_field = 'shop_id'
    serializer_class = ShopSerializer
    permission_classes = (permissions.IsAuthenticated, IsShopAdmin)
