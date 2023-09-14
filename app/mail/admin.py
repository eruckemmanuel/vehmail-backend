from django.contrib import admin

from mail.models import (EmailEvent, Mail)


@admin.register(EmailEvent)
class EmailEventAdmin(admin.ModelAdmin):
    list_display = ["event", "user", "subject", "created"]


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ["user", "subject", "date", "seen"]
