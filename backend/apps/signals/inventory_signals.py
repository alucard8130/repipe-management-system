from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.inventory.models import InventoryMovement


@receiver(post_save, sender=InventoryMovement)
def inventory_movement_post_save(sender, instance: InventoryMovement, created, **kwargs):
    """
    Hook para futuros eventos:
    - alertas de stock bajo
    - notificaciones
    """
    if not created:
        return

    # Aquí luego puedes:
    # - disparar alertas
    # - enviar notificaciones
    pass
