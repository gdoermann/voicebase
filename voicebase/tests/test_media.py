import os
from urlparse import urljoin

import requests

from voicebase import settings
from voicebase.tests.lib import BaseTestCase


class TestApiMediaEndpoint(BaseTestCase):
    def test_urls(self):
        self.assertEqual(self.api.base_url(), settings.BASE_URL)
        self.assertEqual(self.api.media.full_url('base'), urljoin(self.api.base_url(), '{}/media'.format(settings.API_VERSION)))

    def test_media_list(self):
        self.assertIsInstance(self.api.media.list(), list)

    def test_media_list_unauthorized(self):
        self.assertRaises(requests.RequestException, self.unauthorized_api.media.list, )

    def test_upload(self):
        media_file = os.path.join(os.path.dirname(__file__), 'testing.mp3')
        self.assertTrue(os.path.exists(media_file))
        mf = self.api.media.upload(media_file, )
        self.assertTrue(str(mf.url).startswith(self.api.base_url()), 'URL does not start with {}'.format(self.api.base_url()))

        return mf

    def test_upload_with_meta(self):
        self.not_implemented()

    def test_upload_with_configuration(self):
        self.not_implemented()

    def test_get_media(self):
        orig = self.test_upload()
        new = self.api.media.get(orig.id)
        self.assertEqual(orig.id, new.id)
        self.assertEqual(orig.url, new.url)

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