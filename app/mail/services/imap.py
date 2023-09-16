import logging
from django.conf import settings
from imapclient import IMAPClient

from account.models import User
from account.utils import get_user_credentials
from mail.utils.constants import IMAP_MESSAGE_HEADER, IMAP_FULL_MESSAGE

logger = logging.getLogger(__name__)


class IMAPService(object):
    session: IMAPClient = None
    host: str = getattr(settings, 'IMAP_HOST', 'mail.vehseh.com')
    folder: str = 'INBOX'

    def __init__(self, user: User, folder: str = None):
        self.user = user
        self._create_session()
        if folder:
            self.folder = folder

        self.select_folder(self.folder)

    def _create_session(self):
        username, password = get_user_credentials(self.user)
        session = IMAPClient(self.host, use_uid=True)
        session.login(username, password)
        self.session = session

    def get_session(self):
        return self.session

    def select_folder(self, folder: str):
        self.folder = folder
        self.session.select_folder(folder)

    def get_user_mail_uuids(self) -> tuple:
        mail_uuids = self.session.search()
        return mail_uuids

    def get_mail_headers(self, mail_uuids: tuple):
        return self.session.fetch(mail_uuids, IMAP_MESSAGE_HEADER)

    def get_full_messages(self, mail_uuids: tuple):
        return self.session.fetch(mail_uuids, IMAP_FULL_MESSAGE)

    def get_mail_flags(self, mail_uuids: tuple):
        return self.session.get_flags(mail_uuids)

    def get_user_folders(self):
        folders = self.session.list_folders()
        return [{'title': item[-1]} for item in folders]


