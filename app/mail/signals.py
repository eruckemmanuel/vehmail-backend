import logging

from django.dispatch import receiver
from django.db.models.signals import post_save

from mail.models import EmailEvent, Mail
from mail.tasks import process_dovecot_push_event_async


@receiver(post_save, sender=EmailEvent)
def _listen_for_new_email_event(sender, instance: EmailEvent, **kwargs):
    if not instance.processed:
        process_dovecot_push_event_async.delay(instance.id)


@receiver(post_save, sender=Mail)
def _listen_for_new_email_received(sender, instance, **kwargs):
    pass
