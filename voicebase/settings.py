import os
from attrdict import AttrDict
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


# The "default" config for everyone.  You can use this as a base.
DEFAULT_CONF = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default.conf')
# The /etc/default (machine level) configuration
ETC_CONF = '/etc/default/voicebase.conf'
# Overrides for the user in ${HOME}/.voicebase.conf
HOME_CONF = '{}/.voicebase.conf'.format(os.environ.get('HOME', '~'))

# Read home last (so it overrides)
all_files = [ETC_CONF, HOME_CONF]
CONFIG_FILES = [DEFAULT_CONF] # We always read in the default
for f in all_files:
    if os.path.exists(f):
        CONFIG_FILES.append(f)

parser = configparser.ConfigParser()
parser.read(CONFIG_FILES)

API_KEY = parser.get('authentication', 'API_KEY')
PASSWORD = parser.get('authentication', 'PASSWORD')

BASE_URL = parser.get('default', 'BASE_URL')
URLS = AttrDict()
for key, base_url in parser.items('api'):
    section = AttrDict({'base': base_url})
    for url_key, value in parser.items('api.{}'.format(key)):
        section[url_key] = '{}/{}'.format(base_url, value)
    URLS[key] = section


TESTING = AttrDict()
TESTING.RAISE_NOT_IMPLEMENTED = parser.getboolean('testing', 'raise_not_implemented')