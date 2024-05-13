# Generated by Django 5.0.6 on 2024-05-13 05:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_task_solution_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subjects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=60, verbose_name='Тема'), blank=True, null=True, size=10),
        ),
    ]
