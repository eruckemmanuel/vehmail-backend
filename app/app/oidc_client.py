import logging

from django.conf import settings

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView

log = logging.getLogger(__name__)


class CreateUserBackend(OIDCAuthenticationBackend):
    """Custom backend for Django OIDC Client

    Modifies base functionality as follows:
    - username is nickname from profile instead of generating hash of email
    - fetch users by username instead of email
        - would create a new user if they change email on edx, and would fail
          because they have the same username
    - Creates AccessControl and Student entries for user
    """
    username_key = 'nickname'

    def create_user(self, claims):
        email = claims.get('email')
        username = self.get_username(claims)
        try:
            user = self.UserModel.objects.get(username=username)
        except:
            user = self.UserModel.objects.create_user(username, email)

        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        # TODO: Needs to be more robust for mult-tenant
        # Currently just selects the first client, which assumes single tenant
        # client = Client.objects.first()
        # if client is not None:
        #     user.client = client
        user.save()

        # # Make sure their student is at least created
        # student, _ = Student.objects.get_or_create(
        #     username=user.username,
        #     defaults={'edx_id': -1})
        #
        # # Create AccessControl so they can access themselves
        # self._create_access_control(user, student)
        return user

    def _create_access_control(self, user, student):
        """Create default AccessControl objects with themselves as student"""
        access, _ = acm.AccessControl.objects.get_or_create(
            instructor=user, access_type=acm.AccessTypes.STUDENTS.value,
            defaults={})
        access.students.add(student)

    def get_username(self, claims):
        """Return username from nickname claim"""
        return claims.get(self.username_key)

    def update_user(self, user, claims):
        """Update the user email"""
        user.email = claims.get('email')
        user.first_name = claims.get('given_name', '')
        user.last_name = claims.get('family_name', '')
        user.save()
        return user

    def verify_claims(self, claims):
        """Ensure nickname and email in returned claims"""
        scopes = self.get_settings('OIDC_RP_SCOPES', 'openid email').split()

        if self.username_key not in claims:
            log.error("nickname missing from claims!")
            return False
        if 'profile' not in scopes:
            log.error("profile missing from scopes!")
            return False
        if 'email' not in scopes:
            log.error("email missing from scopes!")
            return False
        return True

    def filter_users_by_claims(self, claims):
        """Return user based on their username instead of email

        email is mutable in edx, so we're going to look them up by username
        instead.
        """
        username = claims.get('nickname')
        if not username:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(username=username)


class AddSessionState(OIDCAuthenticationCallbackView):
    """Saves the session_state to session if provided.

    Used for detecting if login status has changed at the OP
    """

    def login_success(self):
        log.info("Successful Login")
        state = self.request.GET.get('session_state')
        resp = super().login_success()
        if resp and state:
            self.request.session['session_state'] = state
        return resp
