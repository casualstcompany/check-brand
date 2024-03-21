import redis
from config.config import config

redis_db = redis.Redis(
    host=config.REDIS.HOST,
    port=config.REDIS.PORT,
    db=0,
    password=config.REDIS.PASSWORD,
)
