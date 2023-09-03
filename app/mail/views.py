from rest_framework.views import APIView
from rest_framework.response import Response
from mail.utils.api import get_mails, get_folders
from mail.utils.sample import data


class MailBoxAPIView(APIView):

    def get(self, request):
        messages = get_mails(request)
        return Response(messages)


class MailBoxFolders(APIView):

    def get(self, request):
        return Response(get_folders(request.user))
