
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

def unauthenticateduser(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/")
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func

def loginfirst(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/userlogin")
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):

            group=None
            
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponseRedirect("/")
        return wrapper_func
    return decorator