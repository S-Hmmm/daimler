from multiprocessing import Pool
import time


def f(num):
    time.sleep(1)
    return num


def f1(num):
    print('callback', num)
    return num * 2


if __name__ == '__main__':
    start_time = time.time()
    res_ls = []
    with Pool(processes=4) as p:
        results = [p.apply_async(f, args=(i,), callback=f1) for i in range(30)]
        for res in results:
            res_ls.append(res.get())
    print(res_ls)
    end_time = time.time()
    print(end_time - start_time)
