from .models import Reform
from django.forms import ModelForm, TextInput, DateInput


class ReformForm(ModelForm):
    class Meta:
        model = Reform
        fields = ['number', 'minister', 'ministry', 'budget', 'deadline']

        widgets = {
            'number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер реформы'
            }),
            'minister': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Министр'
            }),
            'ministry': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Министерство'
            }),
            'budget': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Бюджет'
            }),
            'deadline': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сроки сдачи'
            }),
        }