import psycopg2
from psycopg2.extras import execute_batch
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

CONN_INFO = {
    'database': 'hccms',
    'user': 'postgres@faplytics-nonprod-postgres',
    'password': 'I-PJ?=rhvYrZInbpF2gC#eax',
    'host': 'faplytics-nonprod-postgres.postgres.database.chinacloudapi.cn',
    'port': '5432'
}


class PostgreSql:
    def __init__(self, auto_commit=False):
        self.auto_commit = auto_commit
        self._conn = psycopg2.connect(**CONN_INFO)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cursor.close()
        if self.auto_commit:
            self._conn.commit()
        self._conn.close()
        # return True

    def execute(self, *args):
        try:
            if self.auto_commit:
                self._cursor.execute(*args)
                self._conn.commit()
            else:
                self._cursor.execute(*args)
        except psycopg2.Error as e:
            print(e)

    def fetch(self, n='all'):
        if n == 'all':
            return self._cursor.fetchall()
        elif isinstance(n, int) and n > 0:
            return self._cursor.fetchmany(1)
        else:
            raise ValueError('fetch num must be positive integer')

    def commit(self):
        if self._conn:
            self._conn.commit()

    def rollback(self):
        if self._conn:
            self._conn.rollback()

    def close(self):
        if self._conn:
            self._conn.close()


class T1:
    def __init__(self):
        self.simple_pool = SimpleConnectionPool(5, 200, **CONN_INFO)
        self.conn = self.simple_pool.getconn()
        self.conn.autocommit = True

    @contextmanager
    def get_cursor(self):
        try:
            yield self.conn.cursor()
        finally:
            self.simple_pool.putconn(self.conn)

    def query(self, sql, args_ls):
        with self.get_cursor() as cursor:
            execute_batch(cursor, sql, argslist=args_ls)
            print(cursor.fetchall())
