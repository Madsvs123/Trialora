from rest_framework.routers import DefaultRouter

from apps.workitems.views import TaskCommentViewSet, TaskDependencyViewSet, TaskViewSet

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="tasks")
router.register("task-comments", TaskCommentViewSet, basename="task-comments")
router.register("task-dependencies", TaskDependencyViewSet, basename="task-dependencies")
urlpatterns = router.urls
