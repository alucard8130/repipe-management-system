from decimal import Decimal
from django.db import models, transaction

from apps.inventory.models import InventoryMovement, Material
from apps.projects.models import Project
from apps.operations.models import WorkOrder


class InventoryService:
    """
    Lógica de negocio de inventario (Kardex).
    """

    # --------------------------------------------------
    # STOCK
    # --------------------------------------------------
    @staticmethod
    def get_stock(material: Material) -> Decimal:
        """
        Calcula el stock actual de un material.
        """
        total_in = (
            InventoryMovement.objects.filter(
                material=material,
                movement_type=InventoryMovement.TYPE_IN,
            ).aggregate(total=models.Sum("quantity"))["total"]
            or Decimal("0.00")
        )

        total_out = (
            InventoryMovement.objects.filter(
                material=material,
                movement_type=InventoryMovement.TYPE_OUT,
            ).aggregate(total=models.Sum("quantity"))["total"]
            or Decimal("0.00")
        )

        total_adjust = (
            InventoryMovement.objects.filter(
                material=material,
                movement_type=InventoryMovement.TYPE_ADJUST,
            ).aggregate(total=models.Sum("quantity"))["total"]
            or Decimal("0.00")
        )

        return total_in - total_out + total_adjust

    # --------------------------------------------------
    # COSTO PROMEDIO
    # --------------------------------------------------
    @staticmethod
    def get_average_cost(material: Material) -> Decimal:
        """
        Calcula el costo promedio basado en entradas.
        """
        avg_cost = (
            InventoryMovement.objects.filter(
                material=material,
                movement_type=InventoryMovement.TYPE_IN,
            ).aggregate(avg=models.Avg("unit_cost"))["avg"]
            or Decimal("0.00")
        )

        return Decimal(avg_cost)

    # --------------------------------------------------
    # CONSUMO DE MATERIAL
    # --------------------------------------------------
    @staticmethod
    @transaction.atomic
    def consume_material(
        *,
        material: Material,
        quantity: Decimal,
        project: Project,
        work_order: WorkOrder | None = None,
        reference_id: str,
        notes: str = "",
    ) -> InventoryMovement:
        """
        Consume material del inventario y registra el movimiento OUT.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        current_stock = InventoryService.get_stock(material)

        if current_stock < quantity:
            raise ValueError(
                f"Not enough stock for material {material.code}. "
                f"Available: {current_stock}, requested: {quantity}"
            )

        unit_cost = InventoryService.get_average_cost(material)
        total_cost = unit_cost * quantity

        movement = InventoryMovement.objects.create(
            company=material.company,
            material=material,
            movement_type=InventoryMovement.TYPE_OUT,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost,
            project=project,
            work_order=work_order,
            reference_type="CONSUMPTION",
            reference_id=reference_id,
            notes=notes,
        )

        return movement
