from django.conf import settings

from mail.models import EmailEvent


DOVECOT_PUSH_NOTIFICATION_TOKEN = getattr(settings, 'DOVECOT_PUSH_NOTIFICATION_TOKEN', '')


def event_token_is_valid(event_token: str) -> bool:
    return event_token == DOVECOT_PUSH_NOTIFICATION_TOKEN


def save_dovecot_push_event(data: dict) -> None:
    EmailEvent.objects.create(
        uid=data.get('uid'), uid_validity=data.get('uid-validity'),
        subject=data.get('subject'), user=data.get('user'), snippet=data.get('snippet'),
        folder=data.get('folder'), sender=data.get('sender'), event=data.get('event'))


def process_dovecot_push_event(event_id: int) -> None:
    pass

