# timethis.py
# Copied from The Python Cookbook
import time
from functools import wraps
from contextlib import contextmanager


def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__module__}.{func.__name__} : {end - start}')
        return r
    return wrapper


@contextmanager
def timeblock(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f'{label} : {end - start}')

