from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import mailparser

from account.utils import get_user_from_email
from mail.db.mail import save_mail
from mail.models import EmailEvent
from mail.utils.api import (get_imap_session, fetch_mail_headers)


DOVECOT_PUSH_NOTIFICATION_TOKEN = getattr(settings, 'DOVECOT_PUSH_NOTIFICATION_TOKEN', '')


def event_token_is_valid(event_token: str) -> bool:
    return event_token == DOVECOT_PUSH_NOTIFICATION_TOKEN


def save_dovecot_push_event(data: dict) -> None:
    EmailEvent.objects.create(
        uid=data.get('imap-uid'), uid_validity=data.get('imap-uidvalidity'),
        subject=data.get('subject'), user=data.get('user'), snippet=data.get('snippet'),
        folder=data.get('folder'), sender=data.get('from'), event=data.get('event'))


def process_dovecot_push_event(event_id: int) -> None:
    try:
        event = EmailEvent.objects.get(id=event_id)
    except ObjectDoesNotExist as e:
        return
    user = get_user_from_email(event.user)
    session = get_imap_session(user)
    mail_headers = fetch_mail_headers(session, (int(event.uid),))

    for uid, msg_data in mail_headers.items():
        content = msg_data[b"BODY[HEADER]"]
        mail = mailparser.parse_from_bytes(content)
        save_mail(user, uid, mail)


