from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from .forms import ShopEditForm
from .models import Shop
from users.decorators import admin_required


@login_required(login_url='/login/')
@admin_required
def shops_view(request):
    shops = Shop.objects.all()
    return render(request, 'shop/shops_list.html', {'shops': shops})


@login_required(login_url='/login/')
@admin_required
def create_shop(request):
    if request.method == 'POST':
        form = ShopEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shops')
        else:
            return render(request, 'shop/create_shop.html', {'form': form})
    else:
        form = ShopEditForm({'users': [request.user]})
        return render(request, 'shop/create_shop.html', {'form': form})


@login_required(login_url='/login/')
@admin_required
def shop_details(request, shop_id):
    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        return HttpResponseBadRequest()
    return render(request, 'shop/shop_details.html', {'shop': shop})


@login_required(login_url='/login/')
@admin_required
def edit_shop(request, shop_id):
    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        return HttpResponseBadRequest()
    if request.method == 'POST':
        form = ShopEditForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shop_details', shop_id=shop_id)
    else:
        form = ShopEditForm(instance=shop)
    return render(request, 'shop/edit_shop.html', {'form': form, 'shop': shop})


@login_required(login_url='/login/')
@admin_required
def delete_shop(request, shop_id):
    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        return HttpResponseBadRequest()
    shop.delete()
    return redirect('shops')
