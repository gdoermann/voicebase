import urllib
from urlparse import urljoin

from voicebase import settings


class BaseApiEndpoint(object):
    URLS = {}

    def __init__(self, api):
        self.api = api

    @property
    def session(self):
        return self.api.session

    @property
    def token(self):
        return self.api.token

    def full_url(self, key, base=None):
        if not base:
            base = self.api.base_url()
        return urljoin(base, self.URLS[key])