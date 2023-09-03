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


def extract_message_payload(msg):
    return {
        "from": msg.from_,
        "to": msg.to,
        "cc": msg.cc,
        "message_id": msg.message_id,
        "subject": msg.subject,
        "attachments": msg.attachments,
        "date": msg.date,
        "text_html": msg.text_html,
        "text_plain": msg.text_plain,
        "flags": msg.flags
    }


def paginate_threads(threads, request):
    paginator = MailboxPageNumberPagination()
    page = paginator.paginate_queryset(threads, request)
    return page, paginator


def get_mails(request) -> list[dict]:
    user = request.user
    session = get_imap_session(user)
    session.select_folder('INBOX')
    threads = session.thread()
    threads = tuple(reversed(threads))
    page, paginator = paginate_threads(threads, request)
    messages = []
    for thread in page:
        thread_messages = []
        for mini_thread in thread:
            fetched_messages = session.fetch(mini_thread, 'RFC822')
            for uuid, msg_data in fetched_messages.items():
                content = msg_data[b"RFC822"]
                msg = mailparser.parse_from_bytes(content)
                thread_messages.append(extract_message_payload(msg))

        messages.append(thread_messages)

    return paginator.get_paginated_response(messages)


def get_folders(user):
    session = get_imap_session(user)
    folders = session.list_folders()
    return [{'title': item[-1]} for item in folders]
