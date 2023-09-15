from rest_framework import serializers

from mail.models import Mail


class MailSerializer(serializers.ModelSerializer):
    seen = serializers.SerializerMethodField()

    class Meta:
        model = Mail
        fields = ["id", "from", "to", "uid", "subject", "message_id", "in_reply_to", "date", "created", "seen",
                  "cc", "folder", "num_attachments", "snippet"]

    def get_seen(self, mail):
        if mail.seen:
            return True

        if not mail.seen:
            pass
