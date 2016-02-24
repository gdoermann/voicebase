import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser


# The "default" config for everyone.  You can use this as a base.
DEFAULT_CONF = os.path.join(os.path.dirname(__file__), 'default.conf')
# The /etc/default (machine level) configuration
ETC_CONF = '/etc/default/voicebase.conf'
# Overrides for the user in ${HOME}/.voicebase.conf
HOME_CONF = '{}/.voicebase.conf'.format(os.environ.get('HOME', '~'))

# Read home last (so it overrides)
all_files = [ETC_CONF, HOME_CONF]
CONFIG_FILES = [DEFAULT_CONF] # We always read in the default
for f in all_files:
    if not os.path.exists(f):
        CONFIG_FILES.append(f)

parser = configparser.ConfigParser()
parser.read(CONFIG_FILES)

API_KEY = parser.get('authentication', 'API_KEY')
PASSWORD = parser.get('authentication', 'PASSWORD')

BASE_URL = parser.get('api', 'BASE_URL')
