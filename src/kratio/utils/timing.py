import time
from functools import wraps
from loguru import logger

def timed(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            logger.info(f"Time spent {name}: {duration:.2f} ms")
            return result
        return wrapper
    return decorator