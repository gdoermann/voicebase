
class BaseApiEndpoint(object):
    URLS = {}

    def __init__(self, api):
        self.api = api

    @property
    def session(self):
        return self.api.session

    @property
    def token(self):
        return self.api.token