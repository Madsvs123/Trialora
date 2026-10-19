from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.api import make_serializer, make_viewset
from apps.notifications.models import Notification

NotificationSerializer = make_serializer(Notification)


class NotificationViewSet(make_viewset(Notification, NotificationSerializer, ["title", "body"], ["kind", "is_read"], "notifications")):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        item = self.get_object()
        item.is_read = True
        item.read_at = timezone.now()
        item.save(update_fields=["is_read", "read_at"])
        return Response(self.get_serializer(item).data)

    @action(detail=False, methods=["post"])
    def read_all(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True, read_at=timezone.now())
        return Response({"ok": True})
