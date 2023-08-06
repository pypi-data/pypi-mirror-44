import redis


# Get redis connection.

def get_redis(host, port):
    if not host or port:
        host, port = ("localhost", "6379")
    return redis.StrictRedis(host=host, port=port, db=2, charset="utf-8", decode_responses=True)
