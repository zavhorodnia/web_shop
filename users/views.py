from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,  login as django_login, logout as django_logout
from .forms import SignupForm, LoginForm, UserEditForm
from .models import ShopUser
from .decorators import admin_required


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            if user is not None:
                django_login(request, user)
                return redirect('index')
            else:
                context = {'form': form, 'invalid': True}
    else:
        context = {'form': LoginForm()}
    return render(request, 'users/login.html', context)


@login_required(login_url='/login/')
def logout(request):
    django_logout(request)
    return redirect('login')


@login_required(login_url='/login/')
def index(request):
    return render(request, 'users/index.html')


@login_required(login_url='/login/')
@admin_required
def users_view(request):
    users = ShopUser.objects.all()
    return render(request, 'users/users_list.html', {'users': users})


class UserDetails(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, user_id):
        try:
            user = ShopUser.objects.get(id=user_id)
        except ShopUser.DoesNotExist:
            return HttpResponseBadRequest()
        if not request.user.is_admin and request.user.id != user_id:
            print(request.user.id, user_id)
            return render(request, 'users/not_authorized.html', {'id': request.user.id})
        return render(request, 'users/user_details.html', {'user': user})


@login_required(login_url='/login/')
@admin_required
def edit_user(request, user_id):
    try:
        user = ShopUser.objects.get(id=user_id)
    except ShopUser.DoesNotExist:
        return HttpResponseBadRequest()
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_details', user_id=user_id)
    else:
        form = UserEditForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})


@login_required(login_url='/login/')
@admin_required
def delete_user(request, user_id):
    try:
        user = ShopUser.objects.get(id=user_id)
    except ShopUser.DoesNotExist:
        return HttpResponseBadRequest()
    user.delete()
    return redirect('users')
