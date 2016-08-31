import os
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