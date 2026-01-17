from django.db import models
from django.utils import timezone

from apps.core.models import Company


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    """
    Cliente: Homeowner, HOA, Property Manager.
    """
    TYPE_HOMEOWNER = "HOMEOWNER"
    TYPE_HOA = "HOA"
    TYPE_PROPERTY_MANAGER = "PROPERTY_MANAGER"

    TYPE_CHOICES = [
        (TYPE_HOMEOWNER, "Homeowner"),
        (TYPE_HOA, "HOA"),
        (TYPE_PROPERTY_MANAGER, "Property Manager"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="customers")

    customer_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)  # nombre persona o nombre HOA/PM
    company_name = models.CharField(max_length=255, blank=True, default="")  # opcional

    phone = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["company", "customer_type"]),
            models.Index(fields=["company", "name"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.customer_type})"


class Property(TimeStampedModel):
    """
    Propiedad (casa, edificio, multifamiliar).
    """
    TYPE_SINGLE_FAMILY = "SINGLE_FAMILY"
    TYPE_MULTI_FAMILY = "MULTI_FAMILY"

    TYPE_CHOICES = [
        (TYPE_SINGLE_FAMILY, "Single family"),
        (TYPE_MULTI_FAMILY, "Multi-family"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="properties")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="properties")

    property_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=TYPE_SINGLE_FAMILY)
    units_count = models.PositiveIntegerField(default=1)

    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=50, blank=True, default="CA")
    zip_code = models.CharField(max_length=20, blank=True, default="")

    notes = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["company", "city"]),
            models.Index(fields=["company", "state"]),
            models.Index(fields=["company", "zip_code"]),
        ]

    def __str__(self) -> str:
        return f"{self.address_line1}, {self.city}"


class Contact(TimeStampedModel):
    """
    Contacto asociado a Customer o Property (ej: HOA manager, onsite manager, tenant, etc.)
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contacts")

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="contacts",
        null=True,
        blank=True,
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="contacts",
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=255)
    role_title = models.CharField(max_length=255, blank=True, default="")  # ej: HOA Manager
    phone = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["company", "name"]),
            models.Index(fields=["company", "is_primary"]),
        ]

    def __str__(self) -> str:
        return self.name
