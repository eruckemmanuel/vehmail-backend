from django.dispatch import receiver
from django.db.models.signals import post_save

from mail.models import Mail


@receiver(post_save, sender=Mail)
def _listen_for_new_email_received(sender, instance, **kwargs):
    pass
