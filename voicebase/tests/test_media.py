import requests
from voicebase.tests.lib import BaseTestCase


class TestApiMediaEndpoint(BaseTestCase):
    def test_media_list(self):
        self.assertIsInstance(self.api.media.list(), list)

    def test_media_list_unauthorized(self):
        self.assertRaises(requests.RequestException, self.unauthorized_api.media.list, )

    def test_upload(self):
        self.not_implemented()

    def test_get_media(self):
        self.not_implemented()

    def test_delete_media(self):
        self.not_implemented()


class TestVoicebaseMedia(BaseTestCase):
    def test_media_parse(self):
        self.not_implemented()

    def test_get_media_from_cls_method(self):
        self.not_implemented()

    def test_media_transcript_list(self):
        self.not_implemented()

    def test_get_media_transcript(self):
        self.not_implemented()

    def test_get_progress(self):
        self.not_implemented()

    def test_get_streams(self):
        self.not_implemented()

    def test_get_original_stream(self):
        self.not_implemented()

    def test_media_progress(self):
        self.not_implemented()