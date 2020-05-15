from django.shortcuts import render


def admin_required(func):
    def allow_if_admin(request, *args, **kwargs):
        if request.user.is_admin:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'users/not_authorized.html', {'id': request.user.id})
    return allow_if_admin
