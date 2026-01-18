from django.db import models
from django.utils import timezone

from apps.core.models import Company
from apps.projects.models import Project


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# --------------------------------------------------
# INVOICE
# --------------------------------------------------
class Invoice(TimeStampedModel):
    """
    Factura del proyecto.
    """
    STATUS_DRAFT = "DRAFT"
    STATUS_SENT = "SENT"
    STATUS_PARTIAL = "PARTIAL"
    STATUS_PAID = "PAID"
    STATUS_OVERDUE = "OVERDUE"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_SENT, "Sent"),
        (STATUS_PARTIAL, "Partial"),
        (STATUS_PAID, "Paid"),
        (STATUS_OVERDUE, "Overdue"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invoices")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="invoices")

    invoice_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Saldo pendiente",
    )

    language = models.CharField(max_length=5, default="en")  # idioma del PDF

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "invoice_number"],
                name="uq_invoice_company_number",
            )
        ]
        indexes = [
            models.Index(fields=["company", "status"]),
            models.Index(fields=["company", "issue_date"]),
        ]

    def __str__(self) -> str:
        return self.invoice_number

# --------------------------------------------------
# INVOICE ITEM
# --------------------------------------------------
class InvoiceItem(TimeStampedModel):
    """
    Detalle de la factura.
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
    )

    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.invoice.invoice_number} - {self.description}"

# --------------------------------------------------
# PAYMENT
# --------------------------------------------------
class Payment(TimeStampedModel):
    """
    Pago aplicado a una factura (soporta pagos parciales).
    """
    METHOD_CASH = "CASH"
    METHOD_CHECK = "CHECK"
    METHOD_ZELLE = "ZELLE"
    METHOD_ACH = "ACH"
    METHOD_CARD = "CARD"

    METHOD_CHOICES = [
        (METHOD_CASH, "Cash"),
        (METHOD_CHECK, "Check"),
        (METHOD_ZELLE, "Zelle"),
        (METHOD_ACH, "ACH"),
        (METHOD_CARD, "Card"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="payments")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)

    reference = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.invoice.invoice_number} - {self.amount}"
