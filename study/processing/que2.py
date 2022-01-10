from multiprocessing import Pool
from multiprocessing import Manager
import time

PROCESSES = 4


def f():
    q = Manager().Queue()
    items = [(k, v) for k, v in zip(list(range(10)), list(range(10, 20)))]
    for item in items:
        q.put(item)
    for i in range(PROCESSES):
        q.put('STOP')
    with Pool(processes=PROCESSES) as p:
        [p.apply_async(consumer, (q,)) for _ in range(PROCESSES)]
        p.close()
        p.join()


def consumer(it):
    for i, j in iter(it.get, 'STOP'):
        time.sleep(1)
        print(i, j)


if __name__ == '__main__':
    st_time = time.time()
    f()
    end_time = time.time()
    print(end_time - st_time)