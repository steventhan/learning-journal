import os
from passlib.apps import custom_app_context as pwd_context
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated, Everyone
from pyramid.session import SignedCookieSessionFactory


def includeme(config):
    """Security configuration"""
    auth_secret = os.environ['AUTH_SECRET']
    authn_policy = AuthTktAuthenticationPolicy(
            secret=auth_secret,
            hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)
    config.set_default_permission('view')
    config.set_root_factory(AppRoot)
    session_factory = SignedCookieSessionFactory(auth_secret)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)


class AppRoot(object):

    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'modify')
    ]


def check_credentials(username, password):
    stored_username = os.environ['AUTH_USERNAME']
    stored_password = os.environ['AUTH_PASSWORD']
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
