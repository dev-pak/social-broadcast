import redis
from simple_settings import settings

class Storage:
    HOST = 'localhost'
    PORT = 6379
    DB = settings.db

    KEY = 'users'

    def __init__(self):
        self._r = redis.StrictRedis(host=self.HOST, port=self.PORT, db=self.DB)

    def set(self, user_id):
        if self._r.sadd(self.KEY, user_id):
            return True
        return False

    def delete(self, user_id):
        if self._r.srem(self.KEY, user_id):
            return True
        return False

    def all(self):
        return list([int(i) for i in self._r.smembers(self.KEY)])


storage = Storage()
