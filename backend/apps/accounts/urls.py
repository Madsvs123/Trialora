from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    APIKeyViewSet,
    InvitationViewSet,
    InvestigatorViewSet,
    MembershipViewSet,
    RoleViewSet,
    StudyAccessViewSet,
    accept_invite_view,
    forgot_password_view,
    login_view,
    logout_view,
    me_view,
    permissions_catalog_view,
    register_view,
    reset_password_view,
)

router = DefaultRouter()
router.register("roles", RoleViewSet, basename="roles")
router.register("members", MembershipViewSet, basename="members")
router.register("invitations", InvitationViewSet, basename="invitations")
router.register("study-access", StudyAccessViewSet, basename="study-access")
router.register("investigators", InvestigatorViewSet, basename="investigators")
router.register("api-keys", APIKeyViewSet, basename="api-keys")

urlpatterns = [
    path("auth/register/", register_view),
    path("auth/login/", login_view),
    path("auth/logout/", logout_view),
    path("auth/refresh/", TokenRefreshView.as_view()),
    path("auth/me/", me_view),
    path("auth/accept-invite/", accept_invite_view),
    path("auth/forgot-password/", forgot_password_view),
    path("auth/reset-password/", reset_password_view),
    path("auth/permissions/", permissions_catalog_view),
] + router.urls
