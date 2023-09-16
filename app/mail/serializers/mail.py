from rest_framework import serializers

from mail.models import Mail


class MailSerializer(serializers.ModelSerializer):
    uuid = serializers.SerializerMethodField()

    class Meta:
        model = Mail
        fields = ["id", "sender", "to", "uid", "subject", "message_id", "in_reply_to", "date", "created", "seen",
                  "cc", "folder", "num_attachments", "snippet", "sender_name", "sender_email", "uuid"]

    def get_uuid(self, mail):
        return mail.uid


def get_serialized_mails(mails, many=False):
    return MailSerializer(mails, many=many).data


class MailMessageSerializer(serializers.Serializer):
    pass
