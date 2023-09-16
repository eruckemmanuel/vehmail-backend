import logging

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import QuerySet

from account.models import User

logger = logging.getLogger(__name__)

ACCOUNT_DATABASE_KEY = getattr(settings, 'ACCOUNT_DATABASE_KEY', 'account')


def get_remote_user_account(user: User):
    try:
        return User.objects.using(ACCOUNT_DATABASE_KEY).get(email=user.email)
    except ObjectDoesNotExist as e:
        logger.error(e)


def get_user_from_email(email: str) -> User:
    try:
        return User.objects.get(email=email)
    except ObjectDoesNotExist as e:
        logger.error(e)


def get_all_users() -> QuerySet[User]:
    return User.objects.all()
