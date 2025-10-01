import hashlib
import os
import pickle  # nosec
from functools import wraps

import redis


class IntelligentCacheSystem:
    """
    A caching system that connects to Redis and provides
    get/set operations for a cache-aside pattern.
    """

    def __init__(self):
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        try:
            self.redis_client = redis.Redis(
                host=redis_host, port=6379, db=1
            )  # Use db=1 for caching
            self.redis_client.ping()
            print(
                "Intelligent Cache System: Successfully connected to Redis for caching."
            )
        except redis.exceptions.ConnectionError as e:
            print(f"Intelligent Cache System: Could not connect to Redis: {e}")
            self.redis_client = None

    def get(self, key: str):
        if not self.redis_client:
            return None
        try:
            cached_value = self.redis_client.get(key)
            if cached_value:
                print(f"Intelligent Cache System: Cache HIT for key '{key[:50]}...'.")
                return pickle.loads(cached_value)  # nosec
            print(f"Intelligent Cache System: Cache MISS for key '{key[:50]}...'.")
            return None
        except Exception as e:
            print(f"Intelligent Cache System: Error getting from cache: {e}")
            return None

    def set(self, key: str, value: any, ttl: int = 300):
        if not self.redis_client:
            return
        try:
            serialized_value = pickle.dumps(value)
            self.redis_client.setex(key, ttl, serialized_value)
            print(f"Intelligent Cache System: Value SET for key '{key[:50]}...'.")
        except Exception as e:
            print(f"Intelligent Cache System: Error setting to cache: {e}")


# Instantiate a single cache system for the application
cache_system = IntelligentCacheSystem()


def _generate_cache_key(func_name, *args, **kwargs) -> str:
    """
    Generates a consistent cache key based on the function name and its arguments.
    """
    key_parts = [func_name]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))

    # Use a hash to keep the key length manageable and consistent
    key_string = ":".join(key_parts)
    return f"cache:{hashlib.sha256(key_string.encode()).hexdigest()}"


def cached(ttl: int = 300):
    """
    A decorator for implementing the cache-aside pattern.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate a unique cache key from the function's arguments
            cache_key = _generate_cache_key(func.__name__, *args, **kwargs)

            # 1. Try to get from cache
            cached_result = cache_system.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 2. Cache miss: execute the function
            result = func(*args, **kwargs)

            # 3. Store the result in the cache
            if result is not None:
                cache_system.set(cache_key, result, ttl=ttl)

            return result

        return wrapper

    return decorator
