from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimeStampedModel):
    name = models.CharField(max_length=255)
    legal_name = models.CharField(max_length=255, blank=True, default="")
    license_number = models.CharField(max_length=100, blank=True, default="")  # CA license
    phone = models.CharField(max_length=50, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    address_line1 = models.CharField(max_length=255, blank=True, default="")
    address_line2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=50, blank=True, default="CA")
    zip_code = models.CharField(max_length=20, blank=True, default="")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Catalog(TimeStampedModel):
    """
    Contenedor de catálogos: SERVICES, PROJECT_STATUS, MILESTONES, MATERIALS (si lo usas temporalmente), etc.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="catalogs")
    code = models.CharField(max_length=80)  # ej: SERVICES, MILESTONES
    name = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["company", "code"], name="uq_catalog_company_code"),
        ]

    def __str__(self):
        return f"{self.company_id}:{self.code}"


class CatalogItem(TimeStampedModel):
    """
    Item del catálogo: PEX_A_REPIPE, COPPER_L_REPIPE, PLUMBING_WORK, COMPLETED, etc.
    """
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, related_name="items")
    code = models.CharField(max_length=80)      # único dentro del catálogo
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["catalog", "code"], name="uq_catalog_item_catalog_code"),
        ]
        indexes = [
            models.Index(fields=["catalog", "sort_order"]),
            models.Index(fields=["catalog", "code"]),
        ]

    def __str__(self):
        return f"{self.catalog.code}:{self.code}"


class CatalogItemTranslation(TimeStampedModel):
    """
    Traducción EN/ES para cada item.
    """
    LANG_EN = "en"
    LANG_ES = "es"
    LANG_CHOICES = [(LANG_EN, "English"), (LANG_ES, "Español")]

    item = models.ForeignKey(CatalogItem, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=5, choices=LANG_CHOICES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["item", "language"], name="uq_catalog_item_translation_item_lang"),
        ]
        indexes = [
            models.Index(fields=["item", "language"]),
        ]

    def __str__(self):
        return f"{self.item_id}:{self.language}"
