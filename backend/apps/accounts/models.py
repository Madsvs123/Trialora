import hashlib
import secrets
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from apps.common.models import TenantModel, UUIDModel
from apps.common.permissions import PERMISSIONS, ROLE_TEMPLATES


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=140, blank=True)
    avatar_color = models.CharField(max_length=12, default="#1B4D3E")
    timezone = models.CharField(max_length=64, default="UTC")
    is_investigator = models.BooleanField(default=False)
    last_organization = models.ForeignKey(
        "tenants.Organization",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="recent_users",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @property
    def label(self):
        return self.display_name or self.get_full_name() or self.email


class Role(TenantModel):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    description = models.TextField(blank=True)
    is_system = models.BooleanField(default=False)
    permissions = models.JSONField(default=list)

    class Meta:
        unique_together = ("organization", "slug")
        ordering = ["name"]

    @classmethod
    def ensure_defaults(cls, organization):
        for slug, perms in ROLE_TEMPLATES.items():
            cls.objects.get_or_create(
                organization=organization,
                slug=slug,
                defaults={
                    "name": slug.replace("_", " ").title(),
                    "is_system": True,
                    "permissions": perms,
                    "description": f"System {slug.replace('_', ' ')} role",
                },
            )


class Membership(TenantModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="memberships")
    departments = models.ManyToManyField("tenants.Department", blank=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=120, blank=True)

    class Meta:
        unique_together = ("organization", "user")

    def has_perm(self, code: str) -> bool:
        perms = self.role.permissions or []
        return code in perms or "*" in perms


class Invitation(TenantModel):
    email = models.EmailField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="invitations")
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_invitations")
    token = models.CharField(max_length=64, unique=True)
    message = models.TextField(blank=True)
    expires_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    is_investigator = models.BooleanField(default=False)

    class Meta:
        unique_together = ("organization", "email")

    @classmethod
    def issue(cls, organization, email, role, invited_by, days=7, **kwargs):
        return cls.objects.create(
            organization=organization,
            email=email.lower(),
            role=role,
            invited_by=invited_by,
            token=secrets.token_urlsafe(32),
            expires_at=timezone.now() + timezone.timedelta(days=days),
            **kwargs,
        )

    @property
    def is_open(self):
        return self.accepted_at is None and self.expires_at > timezone.now()


class StudyAccess(TenantModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_accesses")
    study = models.ForeignKey("studies.Study", on_delete=models.CASCADE, related_name="accesses")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="study_accesses")
    sites = models.ManyToManyField("sites.Site", blank=True)
    can_view_pii = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    notes = models.CharField(max_length=240, blank=True)

    class Meta:
        unique_together = ("organization", "user", "study")


class InvestigatorProfile(TenantModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="investigator_profile")
    npi_number = models.CharField(max_length=20, blank=True)
    medical_license = models.CharField(max_length=80, blank=True)
    license_state = models.CharField(max_length=80, blank=True)
    specialty = models.CharField(max_length=140, blank=True)
    institution = models.CharField(max_length=180, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    gcp_certified = models.BooleanField(default=False)
    bio = models.TextField(blank=True)


class APIKey(TenantModel):
    name = models.CharField(max_length=120)
    prefix = models.CharField(max_length=12)
    hashed_key = models.CharField(max_length=128)
    scopes = models.JSONField(default=list)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="api_keys")
    last_used_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def hash_key(raw: str) -> str:
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def issue(cls, organization, name, created_by, scopes=None):
        raw = f"trl_{secrets.token_urlsafe(36)}"
        instance = cls.objects.create(
            organization=organization,
            name=name,
            prefix=raw[:10],
            hashed_key=cls.hash_key(raw),
            created_by=created_by,
            scopes=scopes or PERMISSIONS,
        )
        return instance, raw

    @property
    def is_active(self):
        return self.revoked_at is None


class PasswordResetToken(UUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_resets")
    token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def issue(cls, user, hours=2):
        return cls.objects.create(
            user=user,
            token=secrets.token_urlsafe(32),
            expires_at=timezone.now() + timezone.timedelta(hours=hours),
        )

    @property
    def is_open(self):
        return self.used_at is None and self.expires_at > timezone.now()
