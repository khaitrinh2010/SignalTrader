import redis
import json
import os

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, db=0)

def publish_to_redis(channel, message: dict):
    """
    Publish a message to a Redis channel.
    :param channel: The Redis channel to publish to.
    :param message: The message to publish (should be a dictionary).
    """
    # Convert the message to JSON format
    json_message = json.dumps(message)
    
    # Publish the message to the specified channel
    r.publish(channel, json_message)