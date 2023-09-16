import logging

import mailparser

from common.utils.api import MailboxPageNumberPagination
from mail.utils.constants import IMAP_FULL_MESSAGE
from mail.backend.mail import get_imap_session

logger = logging.getLogger(__name__)

IMAP_HOST = 'mail.vehseh.com'


def extract_message_payload(msg, full=False):
    payload = {
        "from": msg.from_,
        "to": msg.to,
        "cc": msg.cc,
        "message_id": msg.message_id,
        "subject": msg.subject,
        "in_reply_to": msg.in_reply_to,
        "num_attachments": len(msg.attachments),
        "date": msg.date,
        "folder": msg.folder
    }
    if full:
        payload["text_html"] = msg.text_html,
        payload["text_plain"] = msg.text_plain
        payload["attachments"] = msg.attachments

    return payload


def paginate_threads(threads, request):
    paginator = MailboxPageNumberPagination()
    page = paginator.paginate_queryset(threads, request)
    return page, paginator


def fetch_thread_messages(session, thread_uuids, return_full_message=False):
    thread_messages = []
    fetched_messages = session.fetch(thread_uuids, IMAP_FULL_MESSAGE)
    for uuid, msg_data in fetched_messages.items():
        content = msg_data[b"RFC822"]
        msg = mailparser.parse_from_bytes(content)
        payload = extract_message_payload(msg, full=return_full_message)
        payload["uuid"] = uuid
        thread_messages.append(payload)

    return thread_messages


def get_mails(request, folder=None) -> list[dict]:
    if not folder:
        folder = 'INBOX'

    user = request.user
    session = get_imap_session(user)
    session.select_folder(folder)
    threads = session.thread()
    threads = tuple(reversed(threads))
    page, paginator = paginate_threads(threads, request)
    mails = []
    for thread in page:
        thread_uuids = ()
        for mini_thread in thread:
            if isinstance(mini_thread, tuple):
                thread_uuids += mini_thread
            else:
                thread_uuids = thread
                break

        mails.append(fetch_thread_messages(session, thread_uuids))

    return paginator.get_paginated_response(mails)

