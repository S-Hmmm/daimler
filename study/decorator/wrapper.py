import functools


def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(text)
            print('begin call %s' % func.__name__)
            result = func(*args, **kwargs)
            print('end call %s' % func.__name__)
            return result
        return wrapper
    return decorator


@log('call func_b')
def func_b():
    print('func_b')


if __name__ == '__main__':
    func_b()
