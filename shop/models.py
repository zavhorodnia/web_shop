from django.db import models
from users.models import ShopUser
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.db.models import Count


class Shop(models.Model):
    shop_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    users = models.ManyToManyField(ShopUser, related_name='shops', blank=False)

    def __str__(self):
        return self.name


def remove_shops_if_orphan(users_pk_set):
    annotated_shops = Shop.objects.annotate(n_owners=Count('users'))
    unreferenced = annotated_shops.filter(pk__in=users_pk_set).filter(n_owners=1)
    unreferenced.delete()


@receiver(pre_delete, sender=ShopUser)
def handle_file_deletion(sender, **kwargs):
    owned_shops = kwargs['instance'].shops.values_list('pk')
    remove_shops_if_orphan(owned_shops)
