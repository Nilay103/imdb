import os
from configparser import RawConfigParser

# fetch base dir path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# we will initialize token and important keys in config file (local)
CONFIG_FILE = os.path.join(BASE_DIR, 'imdb/config.ini')
config = RawConfigParser()
config.read(CONFIG_FILE)

CONST = "THIS IS A NEW CONST WHICH DOESN'T CONFLICT."

# fetching key variables from config files.
SECRET_KEY = config.get('main', 'SECRET_KEY')
MONGODB_URL = config.get('database', 'MONGODB_URL')
DEBUG = config.getboolean('main', 'DEBUG')

DEFAULT_PAGE_LIMIT = 25

CONST_NEW = "THIS CONST MAY GENERATE CONFLICT."
