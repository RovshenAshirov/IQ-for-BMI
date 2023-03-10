from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render, redirect

from iqtest.models import Theme, Dictionary


def is_login(user):
    print(user)
    return user.is_authenticated


# Create your views here.
def index(request: HttpRequest):
    u = User.objects.count()
    t = Theme.objects.count()
    d = Dictionary.objects.count()
    stat = {'user': u, 'category': t, 'test': d}
    return render(request, 'index.html', {'user': request.user, 'stat': stat})


@user_passes_test(is_login, '/login/')
def get_index(request: HttpRequest):
    return render(request, 'index.html')


def login(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(request.GET.get('next', '/'))
    return render(request, 'login.html')


@user_passes_test(is_login, '/login/')
def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('/')


def reg(request: HttpRequest):
    if request.method == 'POST':
        username = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'reg.html')
        try:
            user = User.objects.create_user(username, password=password1)
            auth.login(request, user)
            return redirect(request.GET.get('next', '/'))
        except:
            return render(request, 'reg.html')
    return render(request, 'reg.html')