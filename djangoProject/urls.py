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
    path('info/', views.show_info, name='info'),

# регистрация
    path('', views.show_index, name="home"),

    path('show_minister/<str:direction>/<int:id_user>/addreform/', views.add_reform, name='add_reform'),
    path('show_minister/<str:direction>/<int:id_user>/<int:number_reform>/deletereform/', views.delete_reform, name='delete_reform'),

    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('user_logout', views.logout_user, name='logout_user'),
    path('register_minister/', views.register_minister, name='register_minister'),

    path('bossView/<str:name_ministry>/', views.show_direction_ofMinistry, name='minister_ofMinistry'),
    path('bossView/<str:name_ministry>/<str:direction>/', views.show_ministerFromDirection, name='minister_fromDirection'),
    path('bossView/<str:direction>/<int:id_user>/', views.show_minister, name='show_minister'),
    path('bossMinisterView/<str:direction>/<int:id_minister>/', views.minister_info, name='minister_info'),

    path('ajax/validate_username', views.validate_username, name='validate_username'),
    path('ajax/validate_email', views.validate_email, name='validate_email'),
    path('ajax/check_reform_number/<int:id_minister>/', views.check_numberReform, name='check_reform_number'),
]