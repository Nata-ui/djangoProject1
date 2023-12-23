from django.contrib import admin

# Register your models here.
from django.contrib import admin
from test_django.models import *


# Register your models here.
# admin.site.register(Direction)
# admin.site.register(Department)
# admin.site.register(Minister)
# admin.site.register(Boss)
# admin.site.register(Reform)
# admin.site.register(Ministry)

class MinistryInline(admin.TabularInline):
    model = Ministry
@admin.register(Minister)
class MinisterAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_birth', 'direction')
    list_filter = ('direction', )
    fieldsets = (
        ('ФИ и id министра', {
            'fields': ('last_name', 'first_name', 'id_user')
        }),
        ('Дата рождения и направление', {
            'fields': ('date_birth', 'direction')
        }),
    )
    search_fields = ("last_name__startswith",)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('number', 'description')
@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    def display_direction(self):
        return ",".join([direction.name for direction in self.direction.all()])
    display_direction.short_description = "Направления"
    list_display = ('boss', 'name_ministry', display_direction)

@admin.register(Reform)
class ReformAdmin(admin.ModelAdmin):
    list_display = ('number', 'minister', 'budget', 'deadline')
    list_filter = ('budget', 'minister', 'number', 'deadline')
    fields = ['minister', ('budget', 'number', 'deadline')]



@admin.register(Boss)
class BossAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'department')
    list_filter = ('department', 'last_name')
    inlines = [MinistryInline]
    fieldsets = (
        ('ФИ и id начальника', {
            'fields': ('last_name', 'first_name', 'id_user')
        }),
    )
    search_fields = ("last_name__startswith",)



