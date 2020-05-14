from django.db import models
from users.models import ShopUser


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(ShopUser, related_name='shops', blank=False)
