from django.test import TestCase, Client

from tasks.models import Task, Contest
from tasks.services import get_codeforces_problems, upsert_tasks_from_codeforces, get_distinct_subject_elements, \
    get_distinct_difficulty_elements, get_contest_by_task_difficulty


client = Client()


class TaskTestCase(TestCase):
    def setUp(self):
        Task.objects.create(name_with_index="Sample_1", solution_count=1000, difficulty=1000)

    def test_create_task(self):
        task_1 = Task.objects.get(name_with_index="Sample_1")

        self.assertEqual(task_1.name_with_index, "Sample_1")
        self.assertEqual(task_1.solution_count, 1000)
        self.assertEqual(task_1.difficulty, 1000)
        self.assertEqual(task_1.__str__(), "Sample_1")


class ContestTestCase(TestCase):

    def setUp(self):
        Contest.objects.create(subject="math", difficulty_from=1000, difficulty_to=2000)

    def test_create_contest(self):
        contest_1 = Contest.objects.get(subject="math")

        self.assertEqual(contest_1.subject, "math")
        self.assertEqual(contest_1.difficulty_from, 1000)
        self.assertEqual(contest_1.difficulty_to, 2000)
        self.assertEqual(contest_1.__str__(), "math (1000 - 2000)")


class ServicesTestCase(TestCase):
    result = get_codeforces_problems()
    subjects = get_distinct_subject_elements()
    difficulties = get_distinct_difficulty_elements()
    contest_example = get_contest_by_task_difficulty('math', 1001, 2000)

    def test__result_get_codeforces_problems(self):
        self.assertEqual(type(self.result), list)
        self.assertEqual(list(self.result[0].keys()), [
            'id', 'subjects', 'solution_count', 'name_with_index', 'difficulty'
        ])

    def test_upsert_tasks_from_codeforces(self):
        upsert_tasks_from_codeforces()
        count_tasks = len(Task.objects.all())
        self.assertEqual(count_tasks, len(self.result))

    def test_get_distinct_subject_elements(self):
        subjects_count = len(list(self.subjects))
        self.assertGreater(subjects_count, 0)

    def test_get_distinct_difficulty_elements(self):
        difficulty_count = len(list(self.difficulties))

        self.assertGreater(difficulty_count,0)

    def test_get_contest_by_task_difficulty(self):

        self.assertEqual(self.contest_example.subject, 'math')
        self.assertEqual(self.contest_example.difficulty_from, 1001)
        self.assertEqual(self.contest_example.difficulty_to, 2000)

    def test_create_task(self):

        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 200)
