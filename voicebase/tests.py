import unittest
from voicebase.api import VoicebaseApi

class TestApi(unittest.TestCase):
    def test_settings(self):
        from voicebase import settings
        self.assertIn(settings.DEFAULT_CONF, settings.CONFIG_FILES)
        if not settings.API_KEY:
            self.fail('API Key not set, all tests will fail!')
        if not settings.PASSWORD:
            self.fail('API Password not set, all tests will fail!')

    def test_api_auth(self):
        api = VoicebaseApi()
        token = api.get_auth_token()
        self.assertIsInstance(token, str)
