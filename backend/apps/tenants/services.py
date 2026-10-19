from django.utils.text import slugify

from apps.accounts.models import Membership, Role
from apps.tenants.models import Organization, OrganizationSetting


def unique_slug(name: str) -> str:
    base = slugify(name) or "org"
    slug = base
    index = 1
    while Organization.objects.filter(slug=slug).exists():
        index += 1
        slug = f"{base}-{index}"
    return slug


def provision_organization(*, name, owner, org_type="research", legal_name=""):
    organization = Organization.objects.create(
        name=name,
        slug=unique_slug(name),
        legal_name=legal_name or name,
        org_type=org_type,
    )
    Role.ensure_defaults(organization)
    owner_role = Role.objects.get(organization=organization, slug="owner")
    Membership.objects.create(organization=organization, user=owner, role=owner_role, title="Organization owner")
    OrganizationSetting.objects.get_or_create(organization=organization)
    owner.last_organization = organization
    owner.save(update_fields=["last_organization"])
    return organization
