from celery import shared_task

from mail.services.mails import sync_all_users_mails_from_backend, sync_all_mail_seen_state


@shared_task
def sync_all_users_mails_from_backend_async():
    sync_all_users_mails_from_backend()


@shared_task
def sync_all_mail_seen_state_async():
    sync_all_mail_seen_state()
