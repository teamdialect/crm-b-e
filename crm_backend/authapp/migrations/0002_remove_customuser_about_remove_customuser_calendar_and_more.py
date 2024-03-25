# Generated by Django 5.0.3 on 2024-03-24 08:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='about',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='calendar',
        ),
        migrations.AddField(
            model_name='lead',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]
