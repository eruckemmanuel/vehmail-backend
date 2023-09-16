import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from mail.services.mails import (handle_list_mails, handle_get_mail_message, handle_get_user_folders)


logger = logging.getLogger(__name__)


class ListMailAPIView(APIView):

    def get(self, request):
        return Response(handle_list_mails(request))


class MailMessageAPIView(APIView):

    def get(self, request):
        return Response(handle_get_mail_message(request))


class MailBoxFolders(APIView):

    def get(self, request):
        return Response(handle_get_user_folders(request))
