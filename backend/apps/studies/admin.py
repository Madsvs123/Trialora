from django.contrib import admin

from apps.studies.models import CustomField, Protocol, StatusWorkflow, Study, StudyTemplate

admin.site.register(Study)
admin.site.register(Protocol)
admin.site.register(StudyTemplate)
admin.site.register(CustomField)
admin.site.register(StatusWorkflow)
