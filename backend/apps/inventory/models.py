from django.db import models
from django.utils import timezone

from apps.core.models import Company
from apps.projects.models import Project
from apps.operations.models import WorkOrder


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# --------------------------------------------------
# MATERIAL
# --------------------------------------------------
class Material(TimeStampedModel):
    """
    Catálogo de materiales (inventario centralizado).
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="materials")

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=20)  # ft, pcs, box
    category = models.CharField(max_length=50)  # PEX, Copper, Valve, Drywall

    min_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="uq_material_company_code",
            )
        ]
        indexes = [
            models.Index(fields=["company", "category"]),
            models.Index(fields=["company", "code"]),
        ]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

# --------------------------------------------------
# SUPPLIER
# --------------------------------------------------
class Supplier(TimeStampedModel):
    """
    Proveedores de material.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="suppliers")

    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    payment_terms = models.CharField(max_length=100, blank=True, default="")

    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

# --------------------------------------------------
# PURCHASE ORDER
# --------------------------------------------------
class PurchaseOrder(TimeStampedModel):
    """
    Orden de compra de materiales.
    """
    STATUS_DRAFT = "DRAFT"
    STATUS_ORDERED = "ORDERED"
    STATUS_RECEIVED = "RECEIVED"
    STATUS_CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_ORDERED, "Ordered"),
        (STATUS_RECEIVED, "Received"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="purchase_orders")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name="purchase_orders")

    po_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    order_date = models.DateField(default=timezone.now)
    received_date = models.DateField(null=True, blank=True)

    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "po_number"],
                name="uq_po_company_number",
            )
        ]

    def __str__(self) -> str:
        return self.po_number

# --------------------------------------------------
# PURCHASE ORDER ITEM
# --------------------------------------------------
class PurchaseOrderItem(TimeStampedModel):
    """
    Ítems de la orden de compra.
    """
    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items",
    )
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name="purchase_items")

    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=4)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.purchase_order.po_number} - {self.material.code}"

# --------------------------------------------------
# INVENTORY MOVEMENT (KARDEX)
# --------------------------------------------------
class InventoryMovement(TimeStampedModel):
    """
    Movimientos de inventario (IN / OUT / ADJUST).
    """
    TYPE_IN = "IN"
    TYPE_OUT = "OUT"
    TYPE_ADJUST = "ADJUST"

    TYPE_CHOICES = [
        (TYPE_IN, "In"),
        (TYPE_OUT, "Out"),
        (TYPE_ADJUST, "Adjustment"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory_movements")
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name="movements")

    movement_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=4)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2)

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_movements",
    )
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_movements",
    )

    reference_type = models.CharField(max_length=50)  # PO / CONSUMPTION / ADJUST
    reference_id = models.CharField(max_length=100)

    notes = models.TextField(blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["company", "material"]),
            models.Index(fields=["company", "project"]),
            models.Index(fields=["movement_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.material.code} {self.movement_type} {self.quantity}"

