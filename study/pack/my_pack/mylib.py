import time
from functools import wraps


def timer(func):
    def decorate(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        cost = end - start
        print(f'Run {func.__name__} cost time: {cost}')

        return result
    return decorate


def circle(start, end):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = []
            for i in range(start, end):
                r = func(i, *args, **kwargs)
                result.append(r)
            return result
        return wrapper
    return decorate
