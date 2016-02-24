import json

from voicebase import settings
import requests


class VoicebaseApi(object):
    def __init__(self, api_key=None, password=None, ):
        self.api_key = api_key or settings.API_KEY
        self.password = password or settings.PASSWORD

    def get_auth_token(self):
        url = settings.BASE_URL
        params = dict(apikey=self.api_key, password=self.password)
        return self._api_request(url, params)

    def _api_request(self, url, params, **kwargs):
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
