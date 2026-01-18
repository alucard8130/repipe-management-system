from decimal import Decimal
from django.db import models

from apps.projects.models import Project
from apps.inventory.models import InventoryMovement
from apps.operations.models import TimeEntry
from apps.billing.models import Invoice


class ProjectCostService:
    """
    Lógica de costeo consolidado por proyecto.
    """

    # --------------------------------------------------
    # COSTO DE MATERIAL
    # --------------------------------------------------
    @staticmethod
    def get_material_cost(project: Project) -> Decimal:
        """
        Suma el costo real de material consumido (OUT).
        """
        total = (
            InventoryMovement.objects.filter(
                project=project,
                movement_type=InventoryMovement.TYPE_OUT,
            ).aggregate(total=models.Sum("total_cost"))["total"]
            or Decimal("0.00")
        )

        return total

    # --------------------------------------------------
    # COSTO DE MANO DE OBRA
    # --------------------------------------------------
    @staticmethod
    def get_labor_cost(project: Project) -> Decimal:
        """
        Suma el costo real de horas trabajadas.
        """
        total = (
            TimeEntry.objects.filter(project=project)
            .aggregate(total=models.Sum("total_cost"))["total"]
            or Decimal("0.00")
        )

        return total

    # --------------------------------------------------
    # COSTO TOTAL
    # --------------------------------------------------
    @staticmethod
    def get_total_cost(project: Project) -> Decimal:
        """
        Costo total del proyecto (material + labor).
        """
        material_cost = ProjectCostService.get_material_cost(project)
        labor_cost = ProjectCostService.get_labor_cost(project)

        return material_cost + labor_cost

    # --------------------------------------------------
    # PRECIO DE VENTA
    # --------------------------------------------------
    @staticmethod
    def get_sale_price(project: Project) -> Decimal:
        """
        Precio de venta basado en facturas emitidas.
        """
        total = (
            Invoice.objects.filter(project=project)
            .aggregate(total=models.Sum("total"))["total"]
            or Decimal("0.00")
        )

        return total

    # --------------------------------------------------
    # UTILIDAD Y MARGEN
    # --------------------------------------------------
    @staticmethod
    def get_profit_summary(project: Project) -> dict:
        """
        Devuelve resumen financiero del proyecto.
        """
        sale_price = ProjectCostService.get_sale_price(project)
        total_cost = ProjectCostService.get_total_cost(project)

        profit = sale_price - total_cost

        margin_percent = (
            (profit / sale_price * Decimal("100.0"))
            if sale_price > 0
            else Decimal("0.00")
        )

        return {
            "sale_price": sale_price,
            "material_cost": ProjectCostService.get_material_cost(project),
            "labor_cost": ProjectCostService.get_labor_cost(project),
            "total_cost": total_cost,
            "profit": profit,
            "margin_percent": margin_percent.quantize(Decimal("0.01")),
        }
