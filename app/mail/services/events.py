from django.conf import settings

from account.dao.user import get_user_from_email
from mail.dao.events import get_event_from_id, save_dovecot_push_event, get_pending_events
from mail.services.imap import IMAPService
from mail.services.mails import extract_and_save_user_mail_headers

DOVECOT_PUSH_NOTIFICATION_TOKEN = getattr(settings, 'DOVECOT_PUSH_NOTIFICATION_TOKEN', '')


def handle_dovecot_push_event(data: dict):
    save_dovecot_push_event(data)


def process_dovecot_push_event(event_id: int) -> None:
    event = get_event_from_id(event_id)
    if not event:
        return

    user = get_user_from_email(event.user)
    imap_service = IMAPService(user)
    mail_headers = imap_service.get_mail_headers((int(event.uid),))
    extract_and_save_user_mail_headers(mail_headers, user, event.folder)


def process_pending_dovecot_events():
    events = get_pending_events()
    for event in events:
        process_dovecot_push_event(event.id)


def event_token_is_valid(event_token: str) -> bool:
    return event_token == DOVECOT_PUSH_NOTIFICATION_TOKEN
