# Generated by Django 4.2.5 on 2023-10-10 15:56

from django.db import migrations
import test_django.models


class Migration(migrations.Migration):

    dependencies = [
        ('test_django', '0005_boss_id_user_minister_id_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reform',
            name='number',
            field=test_django.models.IntegerRangeField(default=1, help_text='Введите номер реформы', verbose_name='Номер реформы'),
        ),
    ]
