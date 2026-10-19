from django.contrib import admin

from apps.finance.models import Payment, StudyBudget

admin.site.register(StudyBudget)
admin.site.register(Payment)
