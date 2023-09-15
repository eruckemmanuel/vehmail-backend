import logging

from mailparser import MailParser

from account.models import User
from mail.models import Mail


def save_mail(user: User, uid: str, mail: MailParser):
    Mail.objects.create(sender=mail.from_, to=mail.to, cc=mail.cc, in_reply_to=mail.in_reply_to,
                        uid=uid, subject=mail.subject, message_id=mail.message_id, date=mail.date,
                        user=user, folder=mail.folder)