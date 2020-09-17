import redis
import json
from LuckyStar import settings


class RdConn:
    def __init__(self, **kwargs):
        self.conn = redis.Redis(**kwargs)

    def __dumps(self, value):
        json_value = json.dumps(value, ensure_ascii=False)
        return json_value

    def __loads(self, value):
        return json.loads(value)

    def get(self, name):
        value = self.conn.get(name)
        return value

    def set(self, name, value):
        return self.conn.set(name, value)

    def lpush(self, key, value):
        return self.conn.lpush(key, value)

    def rpop(self, key):
        return self.conn.rpop(key)

    def expire(self, key, time):
        return self.conn.expire(key, time)


def get_redis_helper():
    dbconf = settings.CACHES['default']
    dbconf_setting = settings.CACHES_DEFAULT_PROPERTIES

    rc = RdConn(host=dbconf.get('HOST'),
                port=dbconf.get('PORT'),
                password=dbconf.get('PASSWORD'),
                socket_connect_timeout=dbconf_setting.get('SOCKET_CONNECT_TIMEOUT', 1),
                socket_timeout=dbconf_setting.get('SOCKET_TIMEOUT', 1)
                )
    return rc
