from attrdict import AttrDict

from voicebase import settings
from voicebase.api.base import BaseApiEndpoint


class VoicebaseMediaProgress(object):
    def __init__(self, media, obj):
        self._obj = obj
        self.media = media
        self.progress = AttrDict()
        for k, d in self._obj.get('progress', {}).items():
            self.progress[k] = d.get('status', '')

    @property
    def api(self):
        return self.media.api


class VoicebaseMedia(object):
    def __init__(self, media_obj, api=None):
        self.api = api
        self._obj = media_obj
        self.url = None
        self.id = None
        self.status = None
        self.progress = None
        self.parse()

    def parse(self):
        if not self._obj:
            return
        if not self.api:
            from voicebase.api import VoicebaseApi
            self.api = VoicebaseApi()
        self.url = self._obj.get('_links', {}).get('self', {}).get('href', '')
        self.id = self._obj.get('mediaId', '')
        self.status = self._obj.get('status', '')
        if 'progress' in self._obj:
            self.progress = VoicebaseMediaProgress(self, self._obj.get('progress'))

    @classmethod
    def from_media_id(cls, media_id):
        from voicebase.api import VoicebaseApi
        api = VoicebaseApi()
        return cls(api.media.get(media_id), api=api)

    def transcripts(self):
        """
        Get available transcripts.
        HTTP GET on /media/{mediaId}/transcripts
        :return: VoicebaseTranscripts
        """

    def transcript(self, transcript_id='latest'):
        """
        Get a specific transcript.
        HTTP GET on /media/{mediaId}/transcripts/{transcriptId}
        :param transcript_id:
        :return:
        """

    def get_progress(self):
        """
        Get progress phases.
        HTTP GET on /media/{mediaId}/progress
        Will reload the progress from the server every time it is called!  To get the latest progress use .progress
        :return: VoicebaseMediaProgress
        """

    def get_streams(self):
        """
        Get available media URLs.
        HTTP GET on /media/{mediaId}/streams
        :return: dictionary of name: url
        """

    def get_original_stream(self):
        """
        Redirects to the original version of the file.
        HTTP GET on /media/{mediaId}/streams/original
        :return: original media stream file
        """


class MediaEndpoint(BaseApiEndpoint):
    URLS = settings.URLS.media

    def list(self, external_id=None):
        """
        Retrieve from the media colection.
        HTTP GET on /media
        :param external_id: A unique identifier in an external system, set in metadata on POST.
        :return: list(VoicebaseMedia)
        """

    def upload(self, filename, configuration=None, metadata=None, transcript=None):
        """
        Upload new new media to the service as an attachment or from a url.
        HTTP POST on /media
        :param filename: Media file attached to the request.
        :param configuration: A JSON object with configuration options.
        :param metadata: Metadata about the file being posted.
        :param transcript: attached transcript
        :return: VoicebaseMedia
        """

    def get(self, media_id):
        """
        Get this media item and associated analytics.
        HTTP GET on /media/{mediaId}
        :param media_id: Media ID
        :return: VoicebaseMedia
        """

    def delete(self, media_id):
        """
        Delete this media.
        HTTP DELETE on /media/{mediaId}
        :param media_id: Media ID
        :return: boolean
        """