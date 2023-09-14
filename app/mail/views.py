import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from common.exceptions import RequestUnAuthorizedError
from mail.utils.api import get_mails, get_folders, get_message_details
from mail.utils.sample import data
from mail.utils.events import event_token_is_valid, save_dovecot_push_event

logger = logging.getLogger(__name__)


class MailBoxAPIView(APIView):

    def get(self, request):
        mails = get_mails(request)
        return Response(mails)


class MailMessageAPIView(APIView):

    def get(self, request):
        thread_uuids = request.query_params.get("thread_uuids")
        messages = get_message_details(thread_uuids, request.user)
        return Response(messages)


class MailBoxFolders(APIView):

    def get(self, request):
        return Response(get_folders(request.user))


class MailBoxEventAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, event_token):
        if not event_token_is_valid(event_token):
            raise RequestUnAuthorizedError({"detail": "No authorized"})
        save_dovecot_push_event(request.data)
        return Response({"status": "success"})

    def put(self, request, event_token):
        if not event_token_is_valid(event_token):
            raise RequestUnAuthorizedError({"detail": "No authorized"})
        save_dovecot_push_event(request.data)
        return Response({"status": "success"})
