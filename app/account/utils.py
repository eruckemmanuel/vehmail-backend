import logging
from cryptography.fernet import Fernet

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from account.models import User

logger = logging.getLogger(__name__)

ACCOUNT_DATABASE_KEY = getattr(settings, 'ACCOUNT_DATABASE_KEY', 'account')


def get_remote_user_account(user: User):
    try:
        return User.objects.using(ACCOUNT_DATABASE_KEY).get(email=user.email)
    except ObjectDoesNotExist as e:
        logger.error(e)


def get_remote_user_password(user):
    fernet = Fernet(user.hash_key.encode())
    return fernet.decrypt(user.hash.encode()).decode()


def get_user_from_email(email: str) -> User:
    try:
        return User.objects.get(email=email)
    except ObjectDoesNotExist as e:
        logger.error(e)


def get_user_credentials(user: User) -> tuple:
    account = get_remote_user_account(user)
    return user.email, get_remote_user_password(account)