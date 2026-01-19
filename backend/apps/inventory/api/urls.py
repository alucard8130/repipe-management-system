from django.urls import path
from .views import (
    MaterialListAPIView,
    InventoryMovementListAPIView,
    ConsumeMaterialAPIView,
)

urlpatterns = [
    path("materials/", MaterialListAPIView.as_view(), name="material-list"),
    path("movements/", InventoryMovementListAPIView.as_view(), name="inventory-movements"),
    path("consume/", ConsumeMaterialAPIView.as_view(), name="consume-material"),
]
