from django.contrib.postgres.fields import ArrayField
from django.db import models

from config import settings


NULLABLE = {'null': True, 'blank': True}


class Task(models.Model):
    """Модель задачи"""

    id = models.CharField(max_length=100, verbose_name='id', primary_key=True)
    subjects = ArrayField(models.CharField(max_length=300), verbose_name='Тема', **NULLABLE)
    solution_count = models.IntegerField(verbose_name='Количество решений')
    name_with_index = models.CharField(max_length=300, verbose_name='Название и номер')
    difficulty = models.IntegerField(verbose_name='Сложность')

    def __str__(self):
        return f'{self.name_with_index} ()'


class Contest(models.Model):
    """Модель набора задач, включающего 10 задач одной темы выбранной сложности"""

    tasks = models.ManyToManyField(Task)
    difficulty_from = models.IntegerField(verbose_name='Нижняя граница сложности')
    difficulty_to = models.IntegerField(verbose_name='Верхняя граница сложности')
    subject = models.CharField(max_length=100, verbose_name='Тема')

