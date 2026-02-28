import redis

def redis_is_alive():
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()
        return True
    except Exception:
        return False
