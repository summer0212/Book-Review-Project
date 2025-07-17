import json
import redis
from flask import current_app



redis_client = None

# def get_redis_client():
#     """Initializes and returns the Redis client instance."""
#     global redis_client
#     if redis_client is None:
#         url = current_app.config['REDIS_URL']
#         # This line reads the REDIS_URL from the application's config
#         redis_client = redis.from_url(url,decode_responses=True)
#     return redis_client

BOOKS_CACHE_KEY = "all_books"

def get_from_cache(key):
   
    client = current_app.redis_client
    # client = get_redis_client()

    try:
        
        cached_data = client.get(key)
        if cached_data:
            
            return json.loads(cached_data)

        return None
    except redis.exceptions.ConnectionError as e:
        print(f"CACHE IS DOWN! Could not connect to Redis: {e}")
        return None

def set_in_cache(key, value, ttl=300):
    print("Inside set_in_cache----------------------")
    print(value,"------------------")
    print(key,"------------------")
    # client = get_redis_client()
    client = current_app.redis_client

    try:
        
        print("successfully inside det redis")
        serialized_value = json.dumps(value)
        client.set(key, serialized_value, ex=ttl)
        print(f"Cache SET for key: '{key}' with TTL: {ttl}s")
    except redis.exceptions.ConnectionError as e:
        print(f"CACHE IS DOWN! Could not set key '{key}' in Redis: {e}")

def invalidate_cache(key):
    print("This should not be called after set key")
    """Invalidates/deletes a key from the Redis cache."""
    # client = get_redis_client()
    client = current_app.redis_client
    try:
        client.delete(key)
        print(f"Cache INVALIDATED for key: '{key}'")
    except redis.exceptions.ConnectionError as e:
        print(f"CACHE IS DOWN! Could not invalidate key '{key}' in Redis: {e}")