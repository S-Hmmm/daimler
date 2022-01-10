from threading import Thread
from multiprocessing import Manager
import time


class NewThread(Thread):
    def __init__(self, target, args: iter):
        Thread.__init__(self)
        self.func = target
        self.args = args

    def run(self):
        self.func(*self.args)


def f(q):
    time.sleep(1)
    for k in iter(q.get, 'STOP'):
        print(k)


if __name__ == '__main__':
    start_time = time.time()
    q = Manager().Queue()
    for i in range(30):
        q.put(i)
    for _ in range(10):
        q.put('STOP')
    tasks = [NewThread(target=f, args=(q,)) for _ in range(10)]
    for task in tasks:
        task.start()
    for task in tasks:
        task.join()
    end_time = time.time()
    print(end_time - start_time)
