import hashlib
import os
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from test_django.forms import ReformForm
from test_django.models import Minister, Reform, Boss, Ministry

BASE_DIR = Path(__file__).resolve().parent.parent


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def show_info(request):
    user = request.user

    if user.is_authenticated:
        if user.groups.filter(name="Начальники").exists():
            boss = Boss.objects.get(id_user_id=user.id)
            ministry = list(Ministry.objects.filter(boss_id=boss.id))
            return render(request, 'bossView.html', {"ministry": ministry})
        else:
            minister = Minister.objects.get(id_user_id=user.id)
            reforms = Reform.objects.filter(minister=minister.id)
            reforms = list(reforms)
            return render(request, 'ministerInfo.html',
                          {"minister": minister,
                           "link_img": hashlib.md5(user.email.encode('utf-8')).hexdigest(),
                           "reforms": reforms})
    else:
        return redirect("/")

def show_minister(request, id_user):
    user = request.user
    if user.is_authenticated and user.groups.name == "Начальники":
        minister = Minister.objects.get(id_user_id=id_user)
        reforms = Reform.objects.filter(minister=minister.id)
        reforms = list(reforms)
        return render(request, 'ministerInfo.html',
                      {"minister": minister,
                       "link_img": hashlib.md5(
                           User.objects.get(id=minister.id_user_id).email.encode('utf-8')).hexdigest(),
                       "reforms": reforms})
    else:
        return render(request, 'notAccess.html')


def add_reform(request):
    error = ''
    if request.method == 'POST':
        form = ReformForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reforms_home')
        else:
            error = "Форма заполнена некорректно"

    form = ReformForm()

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'add_reform.html', data)


def success(request):
    return render(request, 'success.html')


def index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect("/info")
        else:
            return render(request, 'index.html')

    else:
        print(request.body)
        if (request.POST.get("email") != None):
            email = request.POST.get("email")
            password = request.POST.get("password")
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)

            try:
                login(request, user)
                return redirect("/info")
            except Exception:
                print("Not correct email or pass")
                return redirect("/")
        else:
            email = request.POST.get("create_email")
            username = request.POST.get("create_user_name")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            return redirect("/info")

