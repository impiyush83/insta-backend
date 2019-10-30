from insta_backend.resources.auth.login import Login
from insta_backend.common import URLS

auth_urls = [
    URLS(resource=Login, endpoint=['login'], name="user_login"),
]
