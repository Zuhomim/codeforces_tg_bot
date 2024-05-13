from tasks.models import Task


class TaskSerializer:
    class Meta:
        model = Task
        fields = "__all__"

