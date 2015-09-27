import json
import redis
from tabulate import tabulate


class RedisClient:

    def __init__(self, redis_host, redis_port, redis_db):
        self.conn = redis.Redis(host=redis_host, port=int(redis_port), db=int(redis_db))

    def keys(self, key_pattern):
        keys = self.conn.keys(key_pattern)
        tab = []
        for key in keys:
            tab.append([key])
        return tabulate(tab,headers=[key_pattern])

    def get(self,key):
        content = self.conn.get(key)
        try:
            data = json.loads(content)
            # return data
            return json.dumps(data,indent=4)
        except Exception:
            return content
