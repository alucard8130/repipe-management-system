from django.db import models
from django.utils import timezone

from apps.core.models import Company, CatalogItem
from apps.projects.models import Project
from apps.users.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# --------------------------------------------------
# WORK ORDER
# --------------------------------------------------
class WorkOrder(TimeStampedModel):
    """
    Orden de trabajo operativa (Plumbing, Drywall, etc.).
    """
    STATUS_OPEN = "OPEN"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="work_orders")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="work_orders")

    trade = models.CharField(max_length=50)  # Plumbing / Drywall
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_work_orders",
    )

    scheduled_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.trade}"

# --------------------------------------------------
# CHECKLIST TEMPLATE
# --------------------------------------------------
class ChecklistTemplate(TimeStampedModel):
    """
    Plantilla de checklist por tipo de trabajo.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="checklist_templates")
    trade = models.CharField(max_length=50)  # Plumbing / Drywall
    name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.trade} - {self.name}"


class ChecklistTemplateItem(TimeStampedModel):
    """
    Ítems de la plantilla.
    """
    template = models.ForeignKey(
        ChecklistTemplate,
        on_delete=models.CASCADE,
        related_name="items",
    )

    label = models.CharField(max_length=255)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.label

# --------------------------------------------------
# WORK ORDER CHECKLIST ITEM
# --------------------------------------------------
class WorkOrderChecklistItem(TimeStampedModel):
    """
    Checklist ejecutado dentro de una WorkOrder.
    """
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="checklist_items",
    )

    template_item = models.ForeignKey(
        ChecklistTemplateItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    label = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.work_order.id} - {self.label}"

# --------------------------------------------------
# TIME ENTRY
# --------------------------------------------------
class TimeEntry(TimeStampedModel):
    """
    Registro de horas trabajadas (costo congelado).
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="time_entries")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="time_entries")
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="time_entries",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="time_entries")

    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)

    hourly_cost_applied = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Costo por hora aplicado al momento del registro",
    )
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.user.email} - {self.hours_worked}h"

# --------------------------------------------------
# PERMIT
# --------------------------------------------------
class Permit(TimeStampedModel):
    """
    Permiso de ciudad.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="permits")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="permits")

    permit_number = models.CharField(max_length=100)
    status = models.CharField(max_length=50, blank=True, default="")

    applied_at = models.DateField(null=True, blank=True)
    issued_at = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.permit_number}"

# --------------------------------------------------
# INSPECTION
# --------------------------------------------------
class Inspection(TimeStampedModel):
    """
    Inspección (Rough / Final / City).
    """
    RESULT_PENDING = "PENDING"
    RESULT_PASS = "PASS"
    RESULT_FAIL = "FAIL"

    RESULT_CHOICES = [
        (RESULT_PENDING, "Pending"),
        (RESULT_PASS, "Pass"),
        (RESULT_FAIL, "Fail"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inspections")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="inspections")

    inspection_item = models.ForeignKey(
        CatalogItem,
        on_delete=models.PROTECT,
        related_name="project_inspections",
    )

    scheduled_at = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default=RESULT_PENDING)
    inspected_at = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True, default="")
    visible_to_client = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.project.project_number} - {self.inspection_item.code}"

