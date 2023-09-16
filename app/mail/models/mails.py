from django.db import models

from common.models import BaseModel


class Mail(BaseModel):
    sender = models.JSONField()
    sender_name = models.CharField(max_length=250, null=True, blank=True)
    sender_email = models.EmailField(max_length=250, null=True, blank=True)
    to = models.JSONField(null=True, blank=True)
    cc = models.JSONField(null=True, blank=True)
    uid = models.CharField(max_length=50)
    folder = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=1000, null=True, blank=True)
    message_id = models.CharField(max_length=1000, unique=True)
    in_reply_to = models.CharField(max_length=1000, null=True, blank=True)
    num_attachments = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    snippet = models.TextField(null=True, blank=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.folder}: {self.user} - {self.subject}"
