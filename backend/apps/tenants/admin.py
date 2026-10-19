from django.contrib import admin

from apps.tenants.models import Country, Department, Organization, OrganizationSetting, Sponsor


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "org_type", "country", "is_active")
    search_fields = ("name", "slug")


admin.site.register(Department)
admin.site.register(Sponsor)
admin.site.register(Country)
admin.site.register(OrganizationSetting)
