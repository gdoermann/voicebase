from voicebase import settings
from voicebase.api.base import BaseApiEndpoint


class VoicebaseToken(object):
    def __init__(self, user, token=None, obj=None):
        if obj is None:
            obj = {}
        self.user = user
        self._obj = obj
        self.token = token
        self.type = None
        self.privileges = None
        self.expires = None
        self._parse_response(obj)

    @property
    def api(self):
        return self.user.api

    def _parse_response(self, obj):
        if not obj:
            return
        if 'type' in obj:
            self.type = obj.get('type', None)
        if 'token' in obj:
            self.token = obj.get('token', None)
        self.privileges = obj.get('privileges', None)
        self.expires = obj.get('expires', None)

    def load_details(self):
        """
        Loads in the token details.
        HTTP GET on
        """
        # TODO: Load from api
        # TODO: call _parse_response to parse details out

    def delete(self):
        """
        Delete and revoke this token.
        HTTP DELETE on /access/users/{userId}/tokens/{token}
        """



class VoicebaseUser(object):
    def __init__(self, endpoint, obj=None):
        self.endpoint = endpoint
        self._obj = obj
        self.id = None
        self.email = None
        self.tokens = []
        self.parse()


    def parse(self):
        if self._obj is None:
            return
        self.id = self._obj.get('id')
        self.email = self._obj.get('email')
        self.tokens = [VoicebaseToken(self, t) for t in self._obj.get('tokens')]

    def load_tokens(self):
        """
        Returns all current tokens for a user
        HTTP GET on /access/users/{userId}/tokens
        Caches in self.tokens
        :return: list of VoicebaseToken objects
        """

    def create_token(self):
        """
        Create a new token.
        HTTP POST on /access/users/{userId}/tokens
        :return: VoicebaseToken object
        """



class AccessEndpoint(BaseApiEndpoint):
    """
    Access and user management operations.
    """
    URLS = settings.URLS.access

    def __init__(self, api):
        super(AccessEndpoint, self).__init__(api)
        self._users = {}

    def users(self):
        """
        View existing users.
        HTTP GET on /access/users
        Will cache users we get from the server.
        :return: list of VoicebaseUser objects
        """
        if not self._users:
            #TODO: Load users!
            pass
        return self._users

    def get_user(self, user_id):
        """
        Details for a specific user.
        Will pull from cached users first, or get and add to cached users.
        :param username: the username or userId of the user
        :return: VoicebaseUser
        """
        if user_id in self._users:
            return self._users.get(user_id)
        else:
            # Load user
            # Save user in cache
            return # return user

