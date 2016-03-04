import unittest

from voicebase import settings
from voicebase.api import VoicebaseApi


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.api = VoicebaseApi()
        self.unauthorized_api = VoicebaseApi(password='invalid password!')

    def not_implemented(self):
        if settings.TESTING.RAISE_NOT_IMPLEMENTED:
            self.fail('Not Implemented')
