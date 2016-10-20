import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone


def includeme(config):
    """Security configuration"""
    auth_secret = os.environ.get('AUTH_SECRET', 'randomstring')
    authn_policy = AuthTktAuthenticationPolicy(
            secret=auth_secret,
            hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(AppRoot)


class AppRoot(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'modify')
    ]


def check_credentials(username, password):
    stored_username = os.environ.get('AUTH_USERNAME', '')
    stored_password = os.environ.get('AUTH_PASSWORD', '')
    is_authenticated = False
    if stored_username and stored_password:
        if username == stored_username:
            try:
                is_authenticated = pwd_context.verify(
                        password, stored_password
                )
            except ValueError:
                pass
    return is_authenticated
