import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from common.exceptions import RequestUnAuthorizedError
from mail.services.events import handle_dovecot_push_event, event_token_is_valid

logger = logging.getLogger(__name__)


class MailBoxEventAPIView(APIView):
    permission_classes = [AllowAny]

    def handle_event(self, request, event_token):
        if not event_token_is_valid(event_token):
            raise RequestUnAuthorizedError({"detail": "No authorized"})
        handle_dovecot_push_event(request.data)
        return Response({"status": "success"})

    def post(self, request, event_token):
        return self.handle_event(request, event_token)

    def put(self, request, event_token):
        return self.handle_event(request, event_token)
