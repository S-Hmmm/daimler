from multiprocessing import Process, Lock


def f(l, num):
    l.acquire()
    try:
        print('hello', num)
    finally:
        l.release()


if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f, args=(lock, i)).start()
