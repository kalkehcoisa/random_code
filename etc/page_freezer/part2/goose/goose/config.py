from huey import RedisHuey
import redis

hueymq = RedisHuey(
    name='huey_goose',
    result_store=True,
    store_errors=False,  # don't store the errors
)

# clear all huey stuff from redis
if hueymq.storage.queue_size() > 0:
    r = redis.Redis()
    r.flushdb()
