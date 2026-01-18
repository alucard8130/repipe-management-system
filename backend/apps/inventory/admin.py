from django.contrib import admin
from .models import (
    Material,
    Supplier,
    PurchaseOrder,
    PurchaseOrderItem,
    InventoryMovement,
)

admin.site.register(Material)
admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(InventoryMovement)
