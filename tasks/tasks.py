from celery import shared_task

from tasks.views import create_tasks


@shared_task
def sync_codeforces_tasks():
    """Периодическая задача синхронизации задач и наборов задач"""

    create_tasks()
