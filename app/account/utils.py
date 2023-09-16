import logging
from cryptography.fernet import Fernet

from account.models import User
from account.dao.user import get_remote_user_account

logger = logging.getLogger(__name__)


def get_remote_user_password(user):
    fernet = Fernet(user.hash_key.encode())
    return fernet.decrypt(user.hash.encode()).decode()


def get_user_credentials(user: User) -> tuple:
    account = get_remote_user_account(user)
    return user.email, get_remote_user_password(account)
