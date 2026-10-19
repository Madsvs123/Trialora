from django.contrib import admin

from apps.safety.models import AdverseEvent, SafetySignal, SeriousAdverseEvent

admin.site.register(AdverseEvent)
admin.site.register(SeriousAdverseEvent)
admin.site.register(SafetySignal)
