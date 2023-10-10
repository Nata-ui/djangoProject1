from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models


# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(**kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Direction(models.Model):
    name = models.CharField(max_length=150, primary_key=True, verbose_name="Название направления",
                            help_text="Введите название направления", null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return "Направление: " + self.name

    class Meta:
        db_table = "Direction"


class Department(models.Model):
    number = models.CharField(max_length=20, verbose_name="Номер отдела",
                              help_text="Введите номер отдела", null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return "Отдел: " + self.number

    class Meta:
        db_table = "Department"


class Minister(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя",
                                  help_text="Введите имя", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия",
                                 help_text="Введите имя", null=False, blank=False)
    date_birth = models.DateField(verbose_name="Дата рождения",
                                  help_text="Введите дату рождения", null=False, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="id отдела",
                                   help_text="Введите отдел", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Министр: " + self.first_name + " " + self.last_name

    class Meta:
        db_table = "Minister"


class Boss(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя",
                                  help_text="Введите имя", null=False, blank=False)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия",
                                 help_text="Введите фамилию", null=False, blank=False)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Название направления",
                                  help_text="Выберите направление", null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="выберите id пользователя", null=True, blank=True)

    def __str__(self):
        return "Начальник: " + self.first_name + " " + self.last_name

    class Meta:
        db_table = "Boss"


class Reform(models.Model):
    number = IntegerRangeField(min_value=1, verbose_name="Номер реформы", default=1,
                               help_text="Введите номер реформы", null=False, blank=False)
    minister = models.ForeignKey(Minister, on_delete=models.CASCADE, verbose_name="Министр",
                                 help_text="Выберите министра", null=False, blank=False)
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE, verbose_name="Имя начальника",
                             help_text="Выберите уполномоченного начальника", null=False, blank=False)
    budget = IntegerRangeField(min_value=0, verbose_name="Бюджет",
                               help_text="Введите сумму бюджета", null=False, blank=False)
    deadline = models.DateField(verbose_name="Сроки",
                                help_text="Введите дату сдачи", null=False, blank=False)

    def __str__(self):
        return "Ответственный: " + self.minister.__str__() + " Бюджет: " + self.budget.__str__()

    class Meta:
        db_table = "Reform"
    # file = models.FileField()
