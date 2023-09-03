import logging

log = logging.getLogger('oidc_provider')


def userinfo(claims, user):
    # Populate claims dict.
    claims['email'] = user.email

    return claims
