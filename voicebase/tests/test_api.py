from voicebase.api import VoicebaseApi
from voicebase.tests.lib import BaseTestCase


class TestApi(BaseTestCase):
    def test_settings(self):
        from voicebase import settings
        self.assertIn(settings.DEFAULT_CONF, settings.CONFIG_FILES)
        if not settings.API_KEY:
            self.fail('API Key not set, all tests will fail!')
        if not settings.PASSWORD:
            self.fail('API Password not set, all tests will fail!')
        self.assertIn('media', settings.URLS.keys())

    def test_api_auth(self):
        token = self.api.get_auth_token()
        self.assertIsInstance(token, str)

        token = self.api.token
        self.assertEqual(token, self.api.token) # Test that the token doesn't change!

