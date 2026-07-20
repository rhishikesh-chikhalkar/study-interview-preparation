"""
Implementation of a retry decorator in Python.
"""

import functools
import time


def retry(retry_count, retry_interval):
    """Decorator to retry a function call on failure."""
    def decorator(my_func):
        @functools.wraps(my_func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retry_count + 1):
                try:
                    print(
                        f"Running the retry function (attempt {attempt}/"
                        f"{retry_count}) with interval {retry_interval}s"
                    )
                    result = my_func(*args, **kwargs)
                    print("completed.")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed with error: {e}")
                    if attempt < retry_count:
                        time.sleep(retry_interval)
            raise last_exception
        return wrapper
    return decorator


@retry(retry_count=2, retry_interval=3)
def my_function(name, number):
    print(f"name: {name} number:{number}")


if __name__ == "__main__":
    my_function("Alice", 42)
