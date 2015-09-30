__author__ = 'Esteban'
import os
"""
Influx db
"""
INFLUX_DB_SERVER = os.getenv("DOMUS_INFLUX_DB_SERVER", "localhost")
INFLUX_DB_PORT = os.getenv("DOMUS_INFLUX_DB_PORT", 8086)
INFLUX_DB_USER = os.getenv("DOMUS_INFLUX_DB_USER", "user")
INFLUX_DB_PASSWORD = os.getenv("DOMUS_INFLUX_DB_PASSWORD", "password")
INFLUX_DB_TABLE = os.getenv("DOMUS_INFLUX_DB_TABLE", "domus")


"""
Twitter API
"""
TWITTER_APP_KEY = os.getenv("DOMUS_TWITTER_APP_KEY", "KEY")
TWITTER_APP_SECRET = os.getenv("DOMUS_TWITTER_APP_SECRET", "SECRET")
TWITTER_OAUTH_TOKEN = os.getenv("DOMUS_TWITTER_OAUTH_TOKEN", "OAUTH")
TWITTER_OAUTH_SECRET = os.getenv("DOMUS_TWITTER_TOKEN_SECRET", "OAUT_SECRET")