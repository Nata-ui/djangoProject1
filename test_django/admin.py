from django.contrib import admin

# Register your models here.
from django.contrib import admin
from test_django.models import *

# Register your models here.
admin.site.register(Direction)
admin.site.register(Department)
admin.site.register(Minister)
admin.site.register(Boss)
admin.site.register(Reform)
admin.site.register(Ministry)