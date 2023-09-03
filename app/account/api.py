from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from rest_framework.views import APIView

from account.serializers import get_serialized_user
from account.models import User
from common.utils.api import get_api_response


@login_required
def user_auth(request):
    """
    Auth view that triggers login via SSO and redirects back to next URL
    """
    next_url = request.GET.get('next')
    if not next_url:
        next_url = "/mail"
    return redirect(next_url)


class UserAPIView(APIView):
    """
    User API View
    """

    def get(self, request):
        """
        Return serialized payload of authenticated user
        Args:
            request:

        Returns:
            DjangoRest Response:
        """
        return get_api_response(get_serialized_user(request.user))

    def post(self, request):
        data = request.user
        user = User.objects.create(**data)
        return get_api_response(get_serialized_user(user))
