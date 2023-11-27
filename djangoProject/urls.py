"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from test_django import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', views.show_info),
    path('', views.index),
    path('add_reform/', views.add_reform, name='add_reform'),
    path('success/', views.success, name='success'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('user_logout', views.logout_user, name='logout_user'),
    path('bossView/<str:name_ministry>/', views.show_direction_ofMinistry, name='minister_ofMinistry'),
    path('bossView/<str:name_ministry>/<str:name_direction>/', views.show_ministerFromDirection, name='minister_fromDirection'),
    path('bossView/<str:name_ministry>/<str:name_direction>/<int:id_user>/', views.show_minister, name='show_minister')


]
