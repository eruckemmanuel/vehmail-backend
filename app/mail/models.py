from django.db import models

from common.models import BaseModel


class Mail(BaseModel):
    sender = models.JSONField()
    to = models.JSONField(null=True, blank=True)
    cc = models.JSONField(null=True, blank=True)
    uid = models.CharField(max_length=50)
    folder = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=1000, null=True, blank=True)
    message_id = models.CharField(max_length=500)
    in_reply_to = models.CharField(max_length=500, null=True, blank=True)
    num_attachments = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    seen = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    snippet = models.TextField(null=True, blank=True)
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.folder}: {self.user} - {self.subject}"


class EmailEvent(BaseModel):
    uid = models.CharField(max_length=50)
    event = models.CharField(max_length=50)
    subject = models.CharField(max_length=1000, null=True)
    sender = models.CharField(max_length=250)
    snippet = models.TextField(null=True, blank=True)
    user = models.CharField(max_length=200)
    uid_validity = models.CharField(max_length=100, null=True, blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} => {self.user} : {self.subject}"
