from flask_restful import Api
from insta_backend.urls import urls


def restful_api(app):
    api = Api(app, prefix='/')
    for url in urls:
        api.add_resource(
            url.resource,
            url.name,
            *url.endpoint,
            strict_slashes=False  # /users will work, no trailing /
        )
