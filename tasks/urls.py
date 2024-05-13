from django.urls import path

from tasks import views
from tasks.apps import TasksConfig

app_name = TasksConfig.name

urlpatterns = [
    path('tasks/create/', views.create_tasks, name='task_create'),
]
