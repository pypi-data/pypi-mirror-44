import redis
from flask import current_app


# Get redis connection.
redis_host, redis_port = current_app.config.get("CACHE_SERVER_ADDR", ('localhost', '6379'))

redis = redis.StrictRedis(host=redis_host, port=redis_port, db=2, charset="utf-8", decode_responses=True)
