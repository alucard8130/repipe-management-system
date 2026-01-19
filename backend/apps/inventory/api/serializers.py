from decimal import Decimal
from rest_framework import serializers

from apps.inventory.models import Material, InventoryMovement
from apps.services.inventory_service import InventoryService


class MaterialSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = [
            "id",
            "code",
            "name",
            "unit",
            "category",
            "min_stock",
            "stock",
        ]

    def get_stock(self, obj) -> Decimal:
        return InventoryService.get_stock(obj)


class InventoryMovementSerializer(serializers.ModelSerializer):
    material_code = serializers.CharField(source="material.code", read_only=True)

    class Meta:
        model = InventoryMovement
        fields = [
            "id",
            "movement_type",
            "material_code",
            "quantity",
            "unit_cost",
            "total_cost",
            "reference_type",
            "reference_id",
            "project",
            "work_order",
            "created_at",
        ]
