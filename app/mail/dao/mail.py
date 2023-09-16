import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Q
from mailparser import MailParser

from account.models import User
from mail.models import Mail

logger = logging.getLogger(__name__)


def mail_exist(uid: str) -> bool:
    return Mail.objects.filter(uid=uid).exists()


def save_user_mail(user: User, uid: str, mail: MailParser, folder: str) -> Mail:
    existing_mail = get_mail_from_message_id(mail.message_id)
    if existing_mail:
        return existing_mail

    return Mail.objects.create(sender=mail.from_, to=mail.to, cc=mail.cc, in_reply_to=mail.in_reply_to,
                               uid=uid, subject=mail.subject, message_id=mail.message_id, date=mail.date,
                               user=user, folder=folder, sender_name=mail.from_[0], sender_email=mail.from_[1])


def get_mail_from_uid(uid: str) -> Mail:
    try:
        return Mail.objects.get(uid=uid)
    except ObjectDoesNotExist as e:
        pass


def get_mail_from_message_id(message_id: str) -> Mail:
    try:
        return Mail.objects.get(message_id=message_id)
    except ObjectDoesNotExist as e:
        pass


def filter_mails_for_sender(mails: QuerySet[Mail], sender: str) -> QuerySet[Mail]:
    # TODO: Implement filtering by sender
    return mails


def get_user_mails(user: User, folder: str = None, filters: dict = None) -> QuerySet[Mail]:
    if not folder:
        folder = 'INBOX'
    mails = Mail.objects.filter(Q(user=user) &
                                Q(folder=folder) &
                                Q(Q(in_reply_to__isnull=True) | Q(in_reply_to=''))).order_by('-date')

    if filters and isinstance(filters, dict):
        sender_filter = filters.get("sender")
        if sender_filter:
            mails = filter_mails_for_sender(mails, sender_filter)

    return mails


def get_mail_threads(message_id: str) -> QuerySet[Mail]:
    filter_thread_ids = [message_id]
    threads = Mail.objects.filter(in_reply_to=message_id).order_by('-date')
    if threads:
        for thread in threads:
            filter_thread_ids.append(thread.message_id)
        threads = Mail.objects.filter(in_reply_to__in=filter_thread_ids)
    return threads


def update_mail(uid: str, data: dict):
    Mail.objects.filter(uid=uid).update(**data)
