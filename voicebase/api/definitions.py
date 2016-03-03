from voicebase import settings
from voicebase.api.base import BaseApiEndpoint


class BaseDefinitions(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @property
    def api(self):
        return self.endpoint.api

class VoicebaseKeywordGroup(object):
    def __init__(self, endpoint, obj=None):
        self.obj = obj
        self.endpoint = endpoint
        self.name = None
        self.revision = None
        self.keywords = []
        self.parse()

    def parse(self):
        if not self.obj:
            return
        self.name = self.obj.get('name')
        self.revision = self.obj.get('revision')
        self.keywords = self.obj.get('keywords')

    @property
    def id(self):
        return self.name

    def save(self):
        """
        Create or update group from a set of keywords.
        HTTP PUT on /definitions/keywords/groups/{groupId}
        """

    def delete(self):
        """
        Delete this keyword group.
        HTTP DELETE on /definitions/keywords/groups/{groupId}
        """


class KeywordDefinitions(BaseDefinitions):
    def __init__(self, endpoint):
        """
        Does not do anything out of the gate.  You have to call something on it first.
        :param endpoint:
        :return:
        """
        super(KeywordDefinitions, self).__init__(endpoint)
        self._groups = None

    @property
    def groups(self):
        """
        Get all defined keyword groups.
        HTTP GET on /definitions/keywords/groups
        :return: dictionary of VoicebaseKeywordGroup objects
        """
        if self._groups is None:
            self._groups = {}
            #TODO:  parse groups here
        return self._groups

    def group(self, name):
        """
        Get a specific group by name / id.
        HTTP GET on /definitions/keywords/groups/{groupId}
        Will not re-load a group that is already loaded.
        :param name: the group name (also known as the groupId)
        :return: VoicebaseKeywordGroup
        """
        if name in self.groups:
            return self.groups[name]
        else:
            #TODO: load group here and save in ._groups
            pass


class MediaDefinitions(BaseDefinitions):
    """
    Define extended metadata searchable fields.
    """
    def list_search_fields(self):
        """
        Get searchable fields.
        HTTP GET on /definitions/media/search
        :return: list of searchable fields
        """

    def add_search_fields(self, fields):
        """
        Create or update custom parameters of metadata for search.
        HTTP PUT on /definitions/media/search
        :param fields: list of string search fields to add / update
        :return: revision number
        """


class VoicebasePredictionModel(object):
    def __init__(self, endpoint, obj=None):
        self.obj = obj
        self.endpoint = endpoint
        self.name = None
        self.revision = None
        self.keywords = []
        self.parse()

    def parse(self):
        if not self.obj:
            return
        self.name = self.obj.get('name')
        self.revision = self.obj.get('revision')
        self.keywords = self.obj.get('keywords')


class PredictionDefinitions(BaseDefinitions):
    """
    Manage predicitive models.
    """
    def list_models(self):
        """
        Get all available predictive models.
        HTTP GET on /definitions/predictions/models
        :return: list of VoicebasePredictionModel objects
        """

    def get_model(self, name):
        """
        A predictive model.
        HTTP GET on /definitions/predictions/models/{modelName}
        :param name:
        :return: VoicebasePredictionModel
        """


class DefinitionsEndpoint(BaseApiEndpoint):
    """
    Allows definition of complex behaviors or reusable data sets.
    """
    URLS = settings.URLS.definitions

    def __init__(self, api):
        super(DefinitionsEndpoint, self).__init__(api)
        self.keywords = KeywordDefinitions(self)
        self.media = MediaDefinitions(self)
        self.predictions = PredictionDefinitions(self)
