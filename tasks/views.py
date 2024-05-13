from django.db.models import Func, F, Count
from django.http import HttpResponse

from tasks.models import Task, Contest
from tasks.services import upsert_tasks_from_codeforces, get_distinct_subject_elements, get_tasks_without_contest, \
    set_contest_for_free_tasks


def create_tasks(*args, **kwargs):
    upsert_tasks_from_codeforces()
    set_contest_for_free_tasks()

    return HttpResponse('Success')

