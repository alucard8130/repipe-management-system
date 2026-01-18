from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.operations.models import TimeEntry


@receiver(post_save, sender=TimeEntry)
def time_entry_post_save(sender, instance: TimeEntry, created, **kwargs):
    """
    Hook para:
    - alertas de sobretiempo
    - control de eficiencia
    """
    if not created:
        return

    # No recalculamos nada aquí.
    pass
