import secrets
from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import Company
from apps.customers.models import Customer
from apps.projects.models import Project

# --------------------------------------------------
# CLIENT USER (LOGIN)
# --------------------------------------------------
class ClientUser(models.Model):
    """
    Usuario externo con login (HOA / Property Manager).
    """
    LANG_EN = "en"
    LANG_ES = "es"
    LANG_CHOICES = [
        (LANG_EN, "English"),
        (LANG_ES, "Español"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="client_users")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="client_users")

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, default="")

    language_preference = models.CharField(
        max_length=5,
        choices=LANG_CHOICES,
        default=LANG_EN,
    )

    is_active = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.email

# --------------------------------------------------
# PROJECT CLIENT ACCESS
# --------------------------------------------------
class ProjectClientAccess(models.Model):
    """
    Define qué cliente puede ver qué proyecto y con qué permisos.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="client_accesses")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="project_accesses")

    client_user = models.ForeignKey(
        ClientUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="project_accesses",
    )

    can_view_documents = models.BooleanField(default=True)
    can_view_photos = models.BooleanField(default=True)
    can_view_financials = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "client_user"],
                name="uq_project_client_user",
            )
        ]

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.customer.name}"

# --------------------------------------------------
# PROJECT SHARE LINK (TOKEN)
# --------------------------------------------------
class ProjectShareLink(models.Model):
    """
    Acceso por link seguro (Homeowner).
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="share_links")

    token_hash = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    revoked_at = models.DateTimeField(null=True, blank=True)

    can_view_documents = models.BooleanField(default=True)
    can_view_photos = models.BooleanField(default=True)
    can_view_financials = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_share_links",
    )

    created_at = models.DateTimeField(default=timezone.now)
    last_used_at = models.DateTimeField(null=True, blank=True)

    @staticmethod
    def generate_token():
        """
        Genera token seguro (solo se muestra una vez).
        """
        return secrets.token_urlsafe(32)

    def is_valid(self):
        if self.revoked_at:
            return False
        return timezone.now() < self.expires_at

    def __str__(self) -> str:
        return f"ShareLink - {self.project.project_number}"
