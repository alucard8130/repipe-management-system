from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.billing.models import Payment
from apps.services.billing_service import BillingService


@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance: Payment, created, **kwargs):
    """
    Al registrar un pago, recalcula saldo y estatus de la factura.
    """
    if not created:
        return

    invoice = instance.invoice
    BillingService.apply_payment(invoice, instance)
