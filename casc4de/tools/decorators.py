import functools
import time
from flask import flash

def timer(func):
    """
    Print the runtime of decorated function
    """
    @functools.wraps(func)
    def wrapper_timer(*arg, **kwargs):
        start_time = time.perf_counter()
        value = func(*arg, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'Finished {func.__name__} in {run_time:.4f} secs', "timer")
        return value
    return wrapper_timer