__author__ = 'Esteban'
import os
"""
Influx db
"""
INFLUX_DB_SERVER = os.getenv("DOMUS_INFLUX_DB_SERVER", "localhost").rstrip()
INFLUX_DB_PORT = os.getenv("DOMUS_INFLUX_DB_PORT", 8086)
INFLUX_DB_USER = os.getenv("DOMUS_INFLUX_DB_USER", "user").rstrip()
INFLUX_DB_PASSWORD = os.getenv("DOMUS_INFLUX_DB_PASSWORD", "password").rstrip()
INFLUX_DB_TABLE = os.getenv("DOMUS_INFLUX_DB_TABLE", "domus").rstrip()


"""
Twitter API
"""
TWITTER_APP_KEY = os.getenv("DOMUS_TWITTER_APP_KEY", "KEY").rstrip()
TWITTER_APP_SECRET = os.getenv("DOMUS_TWITTER_APP_SECRET", "SECRET").rstrip()
TWITTER_OAUTH_TOKEN = os.getenv("DOMUS_TWITTER_OAUTH_TOKEN", "OAUTH").rstrip()
TWITTER_OAUTH_SECRET = os.getenv("DOMUS_TWITTER_TOKEN_SECRET", "OAUT_SECRET").rstrip()


""""
Redis Cache
"""
REDIS_SERVER = os.getenv("DOMUS_REDIS_SERVER",'localhost')
REDIS_PORT  =  os.getenv("DOMUS_REDIS_PORT",6379)
REDIS_DATABASE  = os.getenv("DOMUS_REDIS_DATABASE",1)