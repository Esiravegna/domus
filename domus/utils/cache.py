from redis import StrictRedis, ConnectionError
from domus.utils.logger import master_log
log = master_log.name("DOMUS " + __name__)


class RedisCache(object):

    def __init__(self, params):
        self._validate(params)

        if not self.server:
            raise Exception('Redis Server Not Defined')

        try:
            log.debug('Connecting to redis at [%s]?[%s]' % (self.server, self.database))
            self.cache = StrictRedis(self.server, port=self.port, db=self.database)
        except ConnectionError as ex:
            raise Exception("Unable to connect to Redis", ex)

    def get(self, key):
        """
        Fetch a given key from the cache. If the key does not exist, return
        default, which itself defaults to None.
        """
        ckey = self._create_key(key)
        log.debug("Getting the cache key [%s]" % ckey)
        return self.cache.get(ckey)

    def ping(self):
        """
        This command is often used to test if the cache is still alive, or to measure latency.
        """
        log.debug("Ping to the cache")
        return self.cache.ping()

    def store(self, key, value, expires=None):
        """
        Set a value in the cache. If timeout is given, that timeout will be
        used for the key; otherwise the default cache timeout will be used.
        """
        ckey = self._create_key(key)
        log.debug("Storing the cache key [%s]" % ckey)
        return self.cache.set(ckey, value, ex=expires)

    def delete(self, key):
        """
        Delete a key from the cache, failing silently.
        """
        ckey = self._create_key(key)
        log.debug("Deleting the cache key [%s]" % ckey)
        return self.cache.delete(ckey)

    def _validate(self, params):
        """
        Initialize all the needed parameters
        """
        self.server = params.get('server', 'localhost')
        self.port = params.get('port', 6379)
        self.database = params.get('database', 2)
        self.key_prefix = params.get('key_prefix', 'mltools')

    def _create_key(self, key):
        return "%s.%s" % (self.key_prefix, key)