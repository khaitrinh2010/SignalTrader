import redis
import json
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

def publish(channel, message: dict):
    try:
        r.publish(channel, json.dumps(message))
    except Exception as e:
        print(f"[Redis]: Failed to publish: {e}")
