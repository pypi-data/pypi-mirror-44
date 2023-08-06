""" shrunk - Rutgers University URL Shortener

Configuration options for shrunk.
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))
DB_REPL = ""
"""The replica set"""

DEV_LOGINS = True

DB_HOST = "db"
"""The host machine for the database."""

DB_DATABASE = "shrunk"
"""database name"""

DB_PORT = 27017
"""The database's port on the host machine."""

USER_WHITELIST = ["jcc", "anp120","mjw271"]

SSO_ATTRIBUTE_MAP = {
    "SHIB_UID_1": (True, "netid"),
    "SHIB_UID_2": (True, "uid2"),                                                   
    "SHIB_UID_3": (True, "employeeType"),
}
"""Map SSO attributes to session keys"""

SSO_LOGIN_URL = '/login'
"""URL for local shibboleth login"""



SECRET_KEY = "its free real estate"
"""A secret key for Flask."""

SHRUNK_URL = "http://localhost:5000"
"""The public URL for shrunk."""

LINKSERVER_URL = "http://localhost:5000"
"""The public URL for the link server."""

DUAL_SERVER = True

RUTGERS_IP_LIST = ["app", "localhost"]

# HOLD - jcc
LOG_FORMAT = "%(levelname)s %(asctime)s: %(message)s [in %(pathname)s:%(lineno)d]"
"""The format for the logger."""

# as of now, this lives in ~shrunk (the shrunk home directory)
LOG_FILENAME = "/var/log/shrunk.log"
"""The name of the log file."""

MAX_DISPLAY_LINKS = 8
"""The maximum number of links to display per page."""

GEOLITE_PATH = "/opt/shrunk/GeoLite2-City.mmdb"
