import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from mail.models import EmailEvent

logger = logging.getLogger(__name__)


def save_dovecot_push_event(data: dict) -> None:
    EmailEvent.objects.create(
        uid=data.get('imap-uid'), uid_validity=data.get('imap-uidvalidity'),
        subject=data.get('subject'), user=data.get('user'), snippet=data.get('snippet'),
        folder=data.get('folder'), sender=data.get('from'), event=data.get('event'))


def get_event_from_id(event_id: int) -> EmailEvent:
    try:
        return EmailEvent.objects.get(id=event_id)
    except ObjectDoesNotExist as e:
        logger.error(e)


def get_pending_events() -> QuerySet[EmailEvent]:
    return EmailEvent.objects.filter(processed=False)
