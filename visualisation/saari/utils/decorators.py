import time
from contextlib import contextmanager

# Global debug flag
DEBUG = True

def timed(func):
    def wrapper(*args, **kwargs):
        if DEBUG:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds")
            return result
        else:
            return func(*args, **kwargs)
    return wrapper

@contextmanager
def timing(name: str = "Vlock"):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{name} took {end_time - start_time:.4f} seconds")
