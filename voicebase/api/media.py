import json

import magic
import requests
from attrdict import AttrDict

from voicebase import settings
from voicebase.api.base import BaseApiEndpoint


def clean_dict(d, test=lambda v: v):
    """
    Return only keys that meet the test
    :param d: Dictionary
    :param test: the test to run on the value (example override is: "lambda v: v is not None")
    :return: Cleaned dictionary
    """
    return {k: v for k, v in d.items() if test(v)}


class VoicebaseMediaMeta(object):
    """
    {
  "metadata" : {
    "title" : "Best Scene Ever",
    "speakers" : [ "Arthur Dent", "Ford Prefect" ],
    "external" : {
      "id" : "abcd1234",
      "name" : "Something or other"
    },
    "extended" : {
      "location" : "Magrathea",
      "region-of-the-country" : "Northern"
    }
  },
  "positional" : {
    "18.5" : { 
      "event" : "whale hits ground",
      "utterance" : "I wonder if it will be friends with me?"
    }
  }
}
    """
    def __init__(self, title=None, speakers_list=None, external_id=None, external_name=None, extended_location=None,
                 extended_region=None, positional_info=None):
        self.title = title
        self.speakers_list = speakers_list
        self.external_id = external_id
        self.external_name = external_name
        self.extended_location = extended_location
        self.extended_region = extended_region
        self.positional_info = positional_info

    def metadata(self):
        md = dict(title=self.title, speakers = self.speakers_list, external=self.external_info(),
                  extended=self.extended_info())
        return clean_dict(md)

    def external_info(self):
        return clean_dict(dict(id=self.external_id, name=self.external_name))

    def extended_info(self):
        return clean_dict({'location': self.extended_location, 'region-of-the-country': self.extended_region})

    def as_dict(self):
        return clean_dict({
            'metadata': self.metadata(),
            'positional': self.positional_info,
        })

    def __str__(self):
        return json.dumps(self.as_dict())


class VoicebaseMediaConfiguration(object):
    """
    {
  "configuration" : {              
    "template" : {
      "name" : "default"
    },
    "transcripts" : {
      "vocabularies" : [ "investor-relations" ]
    },
    "keywords" : {
      "groups" : [ "mobile-phone" ]
    },
    "predictions" : {
      "models" : {
        "sales-lead" : {
          "output" : "extended.sales-followup"
        },
        "not-a-sales-lead" : {
          "output" : "extended.sales-ignore"
        }
      }
    },
    "publish" : {
      "callbacks" : [
        "https://api.example.org/callbacks/{mediaId}"
      ]
    }
  }
    """
    def __init__(self, template='default', transcript_vocabularies=None,
                 keyword_groups=None, predictions_models=None, callbacks=None):
        """
        Create a configuration that can be used when you load a new media file. 
        :param template:
        :param transcript_vocabularies:
        :param keyword_groups:
        :param predictions_models:
        :param callbacks:
        """
        self.template = template
        self.transcript_vocabularies = transcript_vocabularies
        self.keyword_groups = keyword_groups
        self.predictions_models = predictions_models
        self.callbacks = callbacks

    def as_dict(self):
        return clean_dict({
            'configuration': {
                'template': self.template_info(),
                'transcripts': self.transcript_info(),
                'keywords': self.keyword_info(),
                'predictions': self.prediction_info(),
                'publish': self.publish_info(),
            }
        })

    def __str__(self):
        return json.dumps(self.as_dict())

    def template_info(self):
        return clean_dict(dict(name=self.template))

    def transcript_info(self):
        return clean_dict(dict(vocabularies=self.transcript_vocabularies))

    def keyword_info(self):
        return clean_dict(dict(groups=self.keyword_groups))

    def prediction_info(self):
        return clean_dict(dict(models=self.prediction_model_dict()))

    def publish_info(self):
        return clean_dict(dict(callbacks=self.callbacks))

    def prediction_model_dict(self):
        """
        Converts the list of prediction_models passed in into properly formatted dictionaries
        :return: formatted prediction model dict
        """
        models = {}
        for model in self.predictions_models:
            models[model.name] = model.keywords
        return models


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
        self._url = None
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

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, u):
        surl = str(u)
        if surl.startswith('http'):
            self._url = u
        elif surl.startswith('/'):
            surl = u[1:]
            self._url = '/'.join([self.api.base_url(), surl])

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
        response = self.session.get(self.full_url('base'))
        response.raise_for_status()
        return [VoicebaseMedia(o, self.api) for o in response.json()['media']]

    def upload(self, filename, configuration=None, metadata=None, transcript=None):
        """
        Upload new new media to the service as an attachment or from a url.
        HTTP POST on /media
        :param filename: Media file attached to the request.
        :param configuration: VoicebaseMediaConfiguration
        :param metadata: VoicebaseMediaMeta
        :param transcript: attached transcript
        :return: VoicebaseMedia
        """
        data = {}
        if metadata:
            data['metadata'] = str(metadata)
        if configuration:
            data['configuration'] = str(configuration)

        # Determine mime type
        m = magic.Magic(mime=True)
        mime_type = m.from_file(filename)

        # Open file and pipe to request
        with open(filename) as handle:
            file_info = [('media', (filename, handle, mime_type))]
            rq = requests.Request(b'POST', self.full_url('base'), data=data, headers=self.session.headers,
                                  files=file_info)
            prepared_rq = rq.prepare()
            response = self.session.send(prepared_rq)
            response.raise_for_status()
        return VoicebaseMedia(response.json(), self.api)

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