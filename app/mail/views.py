from rest_framework.views import APIView
from rest_framework.response import Response
from mail.utils.api import get_mails, get_folders, get_message_details
from mail.utils.sample import data


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
