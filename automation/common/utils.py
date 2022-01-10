import time
from datetime import datetime as dt
import itertools
import pytest
import functools


def parametrize(parameters, cases):
    return pytest.mark.parametrize('http, expected', list(parameters), ids=cases)


def parametrize_ls(parameters, cases):
    return pytest.mark.parametrize('http, expected, item_id', list(parameters), ids=cases)


def all_true(iterable):
    for element in iterable:
        if not element:
            return False
    return True


def utc_time():
    utc_now = dt.strftime(dt.utcnow(), "%Y-%m-%dT%H:%M:%S,%fZ")
    return utc_now


class Cartesian(object):
    def __init__(self):
        self._data_list = []

    def add_data(self, data: []):
        self._data_list.append(data)

    def ex_data(self, data: []):
        self._data_list.extend(data)

    def build(self):
        for item in itertools.product(*self._data_list):
            print(list(item))


def total_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(func.__name__ + '运行花费时间：%f' % (end - start))
    return wrapper
