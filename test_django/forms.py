from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput


class ReformForm(forms.Form):
    number = forms.IntegerField(help_text="Введите номер реформы", min_value=1, max_value=12)
    budget = forms.IntegerField(help_text="Введите бюджет для реформы", min_value=1)
    deadline = forms.DateField(help_text="Выберите дату сдачи реформы", widget=DatePickerInput())


class MinisterForm(forms.Form):
    name = forms.CharField(help_text="Введите имя")
    surname = forms.CharField(help_text="Введите фамилию")
    date_birth = forms.DateField(help_text="Выберите дату рождения", widget=DatePickerInput())
    direction = forms.CharField(help_text="Введите номер команды")
