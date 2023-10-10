import hashlib
import os
from pathlib import Path

from django.shortcuts import render
from test_django.models import Minister, Reform

BASE_DIR = Path(__file__).resolve().parent.parent


def show_info(request):
    user = request.user
    if user.is_authenticated:
        minister = Minister.objects.get(id_user_id=user.id)
        reforms = Reform.objects.filter(minister=minister.id)
        reforms = list(reforms)
        return render(request, 'ministerInfo.html',
                      {"minister": minister,
                       "link_img": hashlib.md5(user.email.encode('utf-8')).hexdigest(),
                       "reforms": reforms})
    else:
        return render(request, 'notAccess.html')


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    else:
        pass
