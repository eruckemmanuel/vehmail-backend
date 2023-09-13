import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from mail.utils.api import get_mails, get_folders, get_message_details
from mail.utils.sample import data

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

    def post(self, request):
        logger.info(f"{request.data}", 'the data')
        print(f"\n\n {request.data}", 'the data')
        return Response({"status": "success"})

    def get(self, request):
        logger.info(f"{request.query_params}", 'the data')
        print(f"\n\n{request.query_params}", 'the data')
        return Response({"status": "success"})

    def put(self, request):
        logger.info(f"{request.data}", 'the data')
        print(f"\n\n {request.data}", 'the data')
        return Response({"status": "success"})
