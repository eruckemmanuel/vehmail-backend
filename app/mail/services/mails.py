import logging

from mailparser import mailparser
from rest_framework.request import Request

from account.dao.user import get_all_users
from account.models import User
from common.utils.api import MailboxPageNumberPagination
from mail.dao.mail import save_user_mail, get_user_mails, get_mail_threads, update_mail
from mail.serializers.mail import get_serialized_mails
from mail.services.imap import IMAPService
from mail.utils.api import extract_message_payload

logger = logging.getLogger(__name__)


def extract_and_save_user_mail_headers(mail_headers: dict, user: User, folder: str):
    for uid, msg_data in mail_headers.items():
        content = msg_data[b"BODY[HEADER]"]
        mail = mailparser.parse_from_bytes(content)
        save_user_mail(user, uid, mail, folder)


def sync_user_mails_from_backend(user: User, folder: str = None):
    imap_service = IMAPService(user, folder)
    mail_uuids = imap_service.get_user_mail_uuids()
    mail_headers = imap_service.get_mail_headers(mail_uuids)
    extract_and_save_user_mail_headers(mail_headers, user, folder)


def sync_user_mails_for_all_folders(user: User):
    imap_service = IMAPService(user)
    folders = imap_service.get_user_folders()
    for folder in folders:
        sync_user_mails_from_backend(user, folder.get('title'))


def sync_all_users_mails_from_backend():
    users = get_all_users()
    for user in users:
        sync_user_mails_for_all_folders(user)


def sync_all_mail_seen_state():
    pass


def handle_list_mails(request: Request):
    params = request.query_params
    folder = params.get('folder')
    mails = get_user_mails(request.user, folder, params)
    paginator = MailboxPageNumberPagination()
    page = paginator.paginate_queryset(mails, request)
    page_threads = []
    for mail in page:
        threads = get_mail_threads(mail.message_id)
        mail_threads = [item for item in threads]
        mail_threads.append(mail)
        serialized_mails = get_serialized_mails(mail_threads, many=True)
        page_threads.append(serialized_mails)

    return paginator.get_paginated_response(page_threads)


def handle_get_mail_message(request: Request):
    thread_uuids_str = request.query_params.get("thread_uuids")
    threads_uuids = tuple(thread_uuids_str.split(','))
    folder = request.query_params.get('folder')
    imap_service = IMAPService(request.user, folder)
    fetched_messages = imap_service.get_full_messages(threads_uuids)

    thread_messages = []
    for uid, msg_data in fetched_messages.items():
        content = msg_data[b"RFC822"]
        msg = mailparser.parse_from_bytes(content)
        payload = extract_message_payload(msg, full=True)
        payload["uid"] = uid
        thread_messages.append(payload)
        update_mail(uid, {"seen": True})

    return thread_messages


def handle_get_user_folders(request: Request):
    imap_service = IMAPService(request.user)
    return imap_service.get_user_folders()
