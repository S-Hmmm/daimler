from contextlib import contextmanager, closing


class Query(object):
    def __init__(self, name):
        self.name = name

    def query(self):
        return self.name

    @staticmethod
    def close():
        print('close')


@contextmanager
def query_test(n):
    print('start')
    q = Query(n)
    yield q
    print('end', end='\n\n')


if __name__ == '__main__':
    with query_test('abc') as que:
        result = que.query()
        print(result)

    with closing(Query('bcd')) as q1:
        print('use closing')
        res = q1.query()
        print(res)
