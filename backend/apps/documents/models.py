from django.db import models
from django.utils import timezone

from apps.core.models import Company
from apps.projects.models import Project
from apps.users.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# --------------------------------------------------
# DOCUMENT
# --------------------------------------------------
class Document(TimeStampedModel):
    """
    Documento almacenado en base de datos (BYTEA).
    Preparado para migrar a S3 en el futuro.
    """

    CATEGORY_CONTRACT = "CONTRACT"
    CATEGORY_PERMIT = "PERMIT"
    CATEGORY_INSPECTION = "INSPECTION"
    CATEGORY_PHOTO = "PHOTO"
    CATEGORY_INVOICE = "INVOICE"
    CATEGORY_OTHER = "OTHER"

    CATEGORY_CHOICES = [
        (CATEGORY_CONTRACT, "Contract"),
        (CATEGORY_PERMIT, "Permit"),
        (CATEGORY_INSPECTION, "Inspection"),
        (CATEGORY_PHOTO, "Photo"),
        (CATEGORY_INVOICE, "Invoice"),
        (CATEGORY_OTHER, "Other"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="documents")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_documents",
    )

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100)  # MIME type
    file_size = models.PositiveIntegerField(help_text="Size in bytes")

    # ARCHIVO EN BASE DE DATOS
    file_blob = models.BinaryField()

    # VISIBILIDAD
    visible_to_client = models.BooleanField(default=False)

    # STORAGE (futuro S3)
    storage_type = models.CharField(max_length=20, default="DB")  # DB / S3
    storage_key = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["company", "project"]),
            models.Index(fields=["company", "category"]),
            models.Index(fields=["company", "visible_to_client"]),
        ]

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.file_name}"

