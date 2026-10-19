from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import (
    APIKey,
    InvestigatorProfile,
    Invitation,
    Membership,
    Role,
    StudyAccess,
    User,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "display_name", "is_investigator", "is_staff")
    ordering = ("email",)
    search_fields = ("email", "display_name")


admin.site.register(Role)
admin.site.register(Membership)
admin.site.register(Invitation)
admin.site.register(StudyAccess)
admin.site.register(InvestigatorProfile)
admin.site.register(APIKey)
