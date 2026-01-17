import time


def timeit(func):
    def wrapper(*args, **kwargs):
        print(f"Called {func.__name__}")
        start = time.ticks_ms()
        result = func(*args, **kwargs)
        end = time.ticks_ms()
        elapsed = time.ticks_diff(end, start)
        print(f"{func.__name__} took {elapsed:.6f}s")
        return result

    return wrapper
