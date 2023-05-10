from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth import logout

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(name='Admin').exists():
            logout(request)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def ceo_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(name='CEO').exists():
            logout(request)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def ceo_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(name='CEO').exists():
            logout(request)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def hospital_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(name='Hospital Admin').exists():
            logout(request)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def hospital_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(name='Employee').exists():
            logout(request)
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
