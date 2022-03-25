import time


def timer(func):
    def decorate(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        cost = end - start
        print(f'Run {func.__name__} cost time: {cost}')

        return result
    return decorate
