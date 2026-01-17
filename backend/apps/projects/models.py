from django.db import models
from django.utils import timezone

from apps.core.models import Company, CatalogItem
from apps.customers.models import Customer, Property
from apps.users.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --------------------------------------------------
# PROJECT
# --------------------------------------------------
class Project(TimeStampedModel):
    """
    Proyecto principal (Job).
    """
    STATUS_LEAD = "LEAD"
    STATUS_SCHEDULED = "SCHEDULED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_INSPECTION = "INSPECTION"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CLOSED = "CLOSED"

    STATUS_CHOICES = [
        (STATUS_LEAD, "Lead"),
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_INSPECTION, "Inspection"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CLOSED, "Closed"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="projects")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="projects")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="projects")

    project_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255, default="")

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_LEAD)

    sales_rep = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_projects",
    )

    estimated_start_date = models.DateField(null=True, blank=True)
    estimated_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["company", "status"]),
            models.Index(fields=["company", "project_number"]),
        ]

    def __str__(self) -> str:
        return f"{self.project_number} - {self.title}"

# --------------------------------------------------
# PROJECT SCOPE ITEM (VENTA)
# --------------------------------------------------
class ProjectScopeItem(TimeStampedModel):
    """
    Partidas vendidas al cliente (lo que se cobra).
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="scope_items")

    service_item = models.ForeignKey(
        CatalogItem,
        on_delete=models.PROTECT,
        related_name="project_scope_items",
    )

    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    description_override = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.service_item.code}"

# --------------------------------------------------
# ESTIMATE
# --------------------------------------------------
class Estimate(TimeStampedModel):
    """
    Estimación versionada del proyecto.
    """
    STATUS_DRAFT = "DRAFT"
    STATUS_SENT = "SENT"
    STATUS_APPROVED = "APPROVED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="estimates")

    version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    language = models.CharField(max_length=5, default="en")  # idioma del PDF
    pdf_generated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.project.project_number} - v{self.version}"
    
# --------------------------------------------------
# CONTRACT
# --------------------------------------------------
class Contract(TimeStampedModel):
    """
    Contrato asociado a una estimación.
    """
    STATUS_DRAFT = "DRAFT"
    STATUS_SENT = "SENT"
    STATUS_SIGNED = "SIGNED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_SIGNED, "Signed"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="contracts")
    estimate = models.ForeignKey(Estimate, on_delete=models.PROTECT, related_name="contracts")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    signed_by_name = models.CharField(max_length=255, blank=True, default="")
    signed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Contract - {self.project.project_number}"

# --------------------------------------------------
# PROJECT MILESTONE
# --------------------------------------------------
class ProjectMilestone(TimeStampedModel):
    """
    Avance entendible por cliente.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="milestones")

    milestone_item = models.ForeignKey(
        CatalogItem,
        on_delete=models.PROTECT,
        related_name="project_milestones",
    )

    order = models.PositiveIntegerField(default=0)

    STATUS_PENDING = "PENDING"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_DONE = "DONE"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    visible_to_client = models.BooleanField(default=True)
    public_note = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.milestone_item.code}"

# --------------------------------------------------
# MATERIAL ESTIMADO
# --------------------------------------------------
class ProjectMaterialEstimate(TimeStampedModel):
    """
    Material estimado (para comparar contra real).
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="material_estimates")
    material = models.ForeignKey(
        CatalogItem,
        on_delete=models.PROTECT,
        related_name="material_estimates",
    )

    estimated_qty = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_unit_cost = models.DecimalField(max_digits=12, decimal_places=4)
    estimated_total_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.material.code}"

# --------------------------------------------------
# LABOR RATE POR PROYECTO
# --------------------------------------------------
class ProjectLaborRate(TimeStampedModel):
    """
    Costo por hora editable por proyecto.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="labor_rates")

    trade = models.CharField(max_length=50)  # Plumbing, Drywall
    hourly_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.trade}"

