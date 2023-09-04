import logging
import email
import mailparser

from imapclient import IMAPClient

from account.models import User
from account.utils import get_remote_user_account, get_remote_user_password
from common.utils.api import MailboxPageNumberPagination

logger = logging.getLogger(__name__)

IMAP_HOST = 'mail.vehseh.com'


def get_user_credentials(user: User) -> tuple:
    account = get_remote_user_account(user)
    return user.email, get_remote_user_password(account)


def get_imap_session(user: User) -> IMAPClient:
    username, password = get_user_credentials(user)
    server = IMAPClient(IMAP_HOST, use_uid=True)
    server.login(username, password)
    return server


def extract_message_payload(msg, full=False):
    payload = {
        "from": msg.from_,
        "to": msg.to,
        "cc": msg.cc,
        "message_id": msg.message_id,
        "subject": msg.subject,
        "has_attachments": len(msg.attachments) > 0,
        "date": msg.date,
        "flags": msg.flags
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
    fetched_messages = session.fetch(thread_uuids, 'RFC822')
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


def get_message_details(thread_uuids_str: str, user: User):
    threads_uuids = tuple(thread_uuids_str.split(','))
    session = get_imap_session(user)
    session.select_folder('INBOX')
    return fetch_thread_messages(session, threads_uuids, return_full_message=True)


def get_folders(user):
    session = get_imap_session(user)
    folders = session.list_folders()
    return [{'title': item[-1]} for item in folders]
