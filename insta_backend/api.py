from flask_restful import Api

from insta_backend.resources.auth.common import bp_auth
from insta_backend.routes.auth_urls import auth_urls


def restful_api(app):
    api = Api(bp_auth, prefix='/')
    for url in auth_urls:
        api.add_resource(
            url.resource,
            url.name,
            *url.endpoint,
            strict_slashes=False  # '/users' will work, no trailing /
        )
