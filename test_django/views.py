import hashlib
import os
from pathlib import Path

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from test_django.forms import ReformForm, MinisterForm
from test_django.models import Minister, Reform, Boss, Ministry, Direction

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
                           "reforms": reforms})
    else:
        return redirect("/")


def show_minister(request, direction, id_user):
    user = request.user
    if user.is_authenticated and user.groups.filter(name="Начальники").exists():
        minister = Minister.objects.get(id_user_id=id_user)
        reforms = Reform.objects.filter(minister=minister.id)
        reforms = list(reforms)
        return render(request, 'ministerInfo.html',
                      {"minister": minister,
                       "link_img": hashlib.md5(
                           User.objects.get(id=minister.id_user_id).email.encode('utf-8')).hexdigest(),
                       "reforms": reforms,
                       "direction": direction,
                       })
    else:
        return render(request, 'notAccess.html')


def minister_info(request, direction, id_minister):
    return render(request, 'ministerInfo.html',
                  {"minister": Minister.objects.get(id=id_minister),
                   "reforms": Reform.objects.filter(minister_id=id_minister),
                   "direction": direction
                   })


def register_minister(request):
    if request.method == 'GET':
        form = MinisterForm()
        return render(request, 'registerMinister.html', {'form': form})
    else:
        form = MinisterForm(request.POST)
        if form.is_valid():
            Minister.objects.filter(id_user_id=request.user).update(first_name=form.cleaned_data['name'],
                                                                    last_name=form.cleaned_data['surname'],
                                                                    date_birth=form.cleaned_data['date_birth'],
                                                                    direction=form.cleaned_data['direction'])

            return redirect('/info')


def add_reform(request, direction, id_user):
    if request.method == "GET":
        reformForm = ReformForm()
        return render(request, "add_reform.html",
                      {"form": reformForm, "id_minister": Minister.objects.get(id_user=id_user).id})
    else:
        reformform = ReformForm(request.POST)

        if reformform.is_valid():
            obj = Reform()
            obj.minister = Minister.objects.get(id_user_id=id_user)
            obj.budget = reformform.cleaned_data['budget']
            obj.number = reformform.cleaned_data['number']
            obj.deadline = reformform.cleaned_data['deadline']
            obj.save()
            if User.objects.get(id=id_user).groups.filter(name="Начальники").exists():
                return redirect(f"/bossView/{direction}/{id_user}")
            else:
                return render(request, 'ministerInfo.html', {'minister': Minister.objects.get(id_user_id=id_user),
                                                             'reforms': Reform.objects.filter(
                                                                 minister_id=Minister.objects.get(
                                                                     id_user_id=id_user).id),
                                                             'direction': Minister.objects.get(
                                                                 id_user_id=id_user).direction_id})
        else:
            return redirect("/")


def delete_reform(request, direction, id_user, number_reform):
    minister_id = Minister.objects.get(id_user_id=id_user).id
    reform = Reform.objects.filter(number=number_reform, minister_id=minister_id).delete()
    if User.objects.get(id=id_user).groups.filter(name="Начальники").exists():
        return redirect(f"/bossView/{direction}/{id_user}")
    else:
        return render(request, 'ministerInfo.html', {'minister': Minister.objects.get(id_user_id=id_user),
                                                     'reforms': Reform.objects.filter(
                                                         minister_id=Minister.objects.get(
                                                             id_user_id=id_user).id),
                                                     'direction': direction})


def show_index(request):
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
                return render(request, 'ministerInfo.html', {'minister': Minister.objects.get(id_user_id=user.id),
                                                             'reforms': Reform.objects.filter(
                                                                 minister_id=Minister.objects.get(id_user_id=user.id).id),
                                                             'direction': Minister.objects.get(id_user_id=user.id).direction_name})
            except Exception:
                print("Not correct email or pass")
                return redirect("/")
        else:
            print("kbg")
            email = request.POST.get("create_email")
            username = request.POST.get("create_user_name")
            password = request.POST.get("create_password")
            user = User.objects.create_user(email=email, username=username, password=password)
            login(request, user)
            Minister.objects.create(id_user_id=user.id, date_birth="2011-11-11")
            return redirect("/register_minister")


def show_direction_ofMinistry(request, name_ministry):
    ministry = Ministry.objects.get(name_ministry=name_ministry)
    direction = ministry.direction.filter(ministry=ministry.name_ministry)
    return render(request, 'bossViewDirection.html', {"direction": direction, "name_ministry": name_ministry})


def show_ministerFromDirection(request, direction, name_ministry):
    ministers = Minister.objects.filter(direction=direction)
    ministerAllReforms = []
    ministerLastReforms = []

    for minister in ministers:
        ministerReforms = Reform.objects.filter(minister_id=minister.id)
        if ministerReforms:
            reform_budgets = minister.reform_set.values_list('budget', flat=True)
            sumBudget = sum(reform_budgets)
            lastReforms = max(minister.reform_set.values_list('deadline', flat=True), default=None)
            ministerAllReforms.append(sumBudget)
            ministerLastReforms.append(lastReforms)
        else:
            ministerAllReforms.append(0)
            ministerLastReforms.append(0)

    ministers = zip(ministers, ministerAllReforms, ministerLastReforms)
    return render(request, 'bossViewMinister.html', {
        "ministers": ministers,
        "direction": direction
    })

def validate_username(request):
    username = request.GET.get('create_user_name', None)
    response = {
        'taken': User.objects.filter(username__exact=username).exists()
    }
    return JsonResponse(response)


def validate_email(request):
    email = request.GET.get('create_email', None)
    response = {
        'taken': User.objects.filter(email__exact=email).exists()
    }
    return JsonResponse(response)


def check_numberReform(request, id_minister):
    number = int(request.GET.get('number', None))
    if (number == ""):
        number = 0
    response = {
        'exist': Reform.objects.filter(number=number, minister_id=id_minister).exists()
    }
    return JsonResponse(response)