from django.db import models

from common.models import BaseModel


class EmailEvent(BaseModel):
    uid = models.CharField(max_length=50)
    event = models.CharField(max_length=50)
    folder = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=1000, null=True)
    sender = models.CharField(max_length=250)
    snippet = models.TextField(null=True, blank=True)
    user = models.CharField(max_length=200)
    uid_validity = models.CharField(max_length=100, null=True, blank=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} => {self.user} : {self.subject}"
