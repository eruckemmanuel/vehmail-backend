import logging
import email
import mailparser

from imapclient import IMAPClient

from account.models import User
from account.utils import get_user_credentials
from mail.utils.constants import IMAP_MESSAGE_HEADER

IMAP_HOST = 'mail.vehseh.com'


def get_imap_session(user: User) -> IMAPClient:
    username, password = get_user_credentials(user)
    server = IMAPClient(IMAP_HOST, use_uid=True)
    server.login(username, password)
    return server


def get_user_mail_uuids(user: User, folder=None) -> tuple:
    if not folder:
        folder = 'INBOX'
    session = get_imap_session(user)
    session.select_folder(folder)
    mail_uuids = session.search()
    return mail_uuids


def fetch_mail_headers(session: IMAPClient, mail_uuids: tuple):
    return session.fetch(mail_uuids, IMAP_MESSAGE_HEADER)
