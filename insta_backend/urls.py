from insta_backend.resources.index import Index
from insta_backend.common import URLS

urls = [
    URLS(resource=Index, endpoint=['/'], name="showcases_homepage"),
]
