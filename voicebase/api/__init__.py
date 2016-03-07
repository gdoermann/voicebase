import json
from urlparse import urljoin

from voicebase import settings
import requests
from voicebase.api import media, access, definitions


class VoicebaseApi(object):
    def __init__(self, api_key=None, password=None, ):
        self.api_key = api_key or settings.API_KEY
        self.password = password or settings.PASSWORD
        self._auth_token = None
        self._session = None
        self.media = media.MediaEndpoint(self)
        self.definitions = definitions.DefinitionsEndpoint(self)
        self.access = access.AccessEndpoint(self)

    def base_url(self):
        return settings.BASE_URL

    def get_auth_token(self):
        url = urljoin(self.base_url(), settings.API_VERSION)
        params = dict(apikey=self.api_key, password=self.password)
        raw_response = requests.get(url, params=params)
        raw_response.raise_for_status()
        response = raw_response.json()
        if not (isinstance(response, dict) and response['success']):
            raise ValueError('Invalid response: {}'.format(response))
        return str(response['token'])

    @property
    def token(self):
        if not self._auth_token:
            self._auth_token = self.get_auth_token()
        return self._auth_token

    @property
    def session(self):
        """
        This is what you should use to make requests.  It sill authenticate for you.
        :return: requests.sessions.Session
        """
        if not self._session:
            self._session = requests.Session()
            self._session.headers.update(dict(Authorization='Bearer {0}'.format(self.token)))
        return self._session
