import time

from pack.my_pack.mylib import timer


@timer
def t():
    print('test')
    time.sleep(1.23)


t()
