import logging
import urllib
from urlparse import urljoin

from voicebase import settings

log = logging.getLogger(__name__)

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

    def full_url(self, key, format_dict=None, base=None):
        if not base:
            base = self.api.base_url()
        u = urljoin(base, self.URLS[key])
        if format_dict:
            new_u = u.format(**format_dict)
            log.debug('URL Formatting: url {} --> new url {}, {}'.format(u, new_u, format_dict))
            return u.format(**format_dict)
        else:
            return u

    def _get(self, key, format_dict=None):
        url = self.full_url(key, format_dict)
        result = self.session.get(url)
        result.raise_for_status()
        jsn = result.json()
        log.debug('GET request on {} resulted in: {}'.format(url, jsn))
        return jsn