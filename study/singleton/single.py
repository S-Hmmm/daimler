import threading
import time


# 1
class SingleOne:
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SingleOne, '_instance'):
            with SingleOne._instance_lock:
                if not hasattr(SingleOne, '_instance'):
                    SingleOne._instance = object.__new__(cls)
        return SingleOne._instance


# 2
class SingletonType(type):
    _instance_lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with SingletonType._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class SingleTwo(metaclass=SingletonType):
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    def task():
        c = SingleOne()
        print(c, time.monotonic())

    def task_1():
        j = SingleTwo('j')
        print(j, time.monotonic())

    for i in range(10):
        t = threading.Thread(target=task_1)
        t.start()

