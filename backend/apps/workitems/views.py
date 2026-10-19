from rest_framework import serializers

from apps.common.api import make_serializer, make_viewset
from apps.workitems.models import Task, TaskComment, TaskDependency

TaskSerializer = make_serializer(
    Task,
    extra={"assignee_name": serializers.CharField(source="assignee.label", read_only=True, default="")},
)
TaskCommentSerializer = make_serializer(
    TaskComment,
    extra={"author_name": serializers.CharField(source="author.label", read_only=True)},
)
TaskDependencySerializer = make_serializer(TaskDependency)

TaskViewSet = make_viewset(Task, TaskSerializer, ["title"], ["study", "status", "priority"], "tasks")
TaskCommentViewSet = make_viewset(TaskComment, TaskCommentSerializer, ["body"], ["task"], "task-comments")
# dependencies use same resource map
TaskDependencyViewSet = make_viewset(TaskDependency, TaskDependencySerializer, [], ["task"], "task-dependencies")
