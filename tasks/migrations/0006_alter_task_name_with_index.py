# Generated by Django 5.0.6 on 2024-05-13 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name_with_index',
            field=models.CharField(max_length=300, verbose_name='Название и номер'),
        ),
    ]
