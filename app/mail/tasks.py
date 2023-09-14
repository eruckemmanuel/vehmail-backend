from celery import shared_task

from mail.utils.events import process_dovecot_push_event


@shared_task
def process_dovecot_push_event_async(event_id: int) -> None:
    process_dovecot_push_event(event_id)
