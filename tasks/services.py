from random import choice

import requests
from django.db import connection

from tasks.models import Task, Contest

URL_CODEFORCES_PROBLEMS = 'https://codeforces.com/api/problemset.problems'
FROM_TO = [{"from": 0, "to": 1000}, {"from": 1001, "to": 2000}, {"from": 2001, "to": 3000}, {"from": 3001, "to": 4000}]


def get_codeforces_problems() -> list:
    """Получает список задач с помощью codeforces API"""

    response = requests.get(URL_CODEFORCES_PROBLEMS).json()['result']
    response_problems = response['problems']
    response_problem_stats = response['problemStatistics']
    problems = []
    for i in range(len(response_problems)):
        problem = {
            'id': str(response_problems[i]["contestId"]) + "_" + str(response_problems[i]["index"]),
            'subjects': response_problems[i]['tags'],
            'solution_count': int(response_problem_stats[i]['solvedCount']) if 'solvedCount' in response_problem_stats[
                i] else 0,
            'name_with_index': response_problems[i]['name'] + " " + str(response_problems[i]['contestId']),
            'difficulty': int(response_problems[i]['rating']) if 'rating' in response_problems[i] else 0,
        }

        problems.append(
            problem
        )
    return problems


def upsert_tasks_from_codeforces() -> None:
    """Создает / обновляет список всех задач(tasks) в БД"""

    tasks = get_codeforces_problems()
    postgres_tasks = []
    for task in tasks:
        new_task = Task(
            id=task['id'],
            subjects=task['subjects'],
            solution_count=task['solution_count'],
            name_with_index=task['name_with_index'],
            difficulty=task['difficulty']
        )
        postgres_tasks.append(new_task)
    Task.objects.bulk_create(
        postgres_tasks,
        update_conflicts=True,
        unique_fields=['id'],
        update_fields=['subjects', 'solution_count', 'difficulty', 'name_with_index'],
    )


def get_tasks_without_contest(subject, diff_from, diff_to) -> None:
    """Получает задачи вне набора по 10 штук, создает Contest и записывает в него результирующий список задач"""

    tasks_without_contest = Task.objects.filter(subjects__contains=[subject], difficulty__gte=diff_from,
                                                difficulty__lte=diff_to).exclude(
        contest__subject=subject)

    index = 0
    tasks_for_contest = []

    for task in tasks_without_contest:
        tasks_for_contest.append(task)
        index += 1
        if index % 10 == 0:
            new_contest = Contest.objects.create(subject=subject, difficulty_from=diff_from, difficulty_to=diff_to)
            new_contest.tasks.add(*tasks_for_contest)
            tasks_for_contest = []
        else:
            continue


def get_distinct_subject_elements():
    """Получает список всех тем (subjects) из БД"""

    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT unnest(subjects) as subject FROM tasks_task ORDER BY subject")
        return [row[0] for row in cursor.fetchall()]


def get_distinct_difficulty_elements():
    """Получает список всех сложностей задач"""

    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT difficulty FROM tasks_task ORDER BY difficulty")
        return cursor.fetchall()


def set_contest_for_free_tasks():
    """Записывает contest в БД для несвязанных с набором задач"""

    subjects = get_distinct_subject_elements()
    for subject in subjects:
        for _range in FROM_TO:
            get_tasks_without_contest(subject, _range["from"], _range["to"])


def get_contest_by_task_difficulty(subject, diff_from, diff_to):
    """Возвращает Contest по выбранным фильтрам темы (subject) и диапазону сложности"""

    contest_list = list(Contest.objects.filter(subject=subject, difficulty_from=diff_from, difficulty_to=diff_to))
    contest = choice(contest_list)
    return contest
