import requests


class Client(object):

    def req(self, method):
        m = str.lower(method)
        if m == 'get':
            return self.__get
        elif m == 'post':
            return self.__post
        elif m == 'put':
            return self.__put
        elif m == 'delete':
            return self.__del
        else:
            raise IOError

    @classmethod
    def __get(cls, **kwargs):
        resp = requests.get(**kwargs)
        return resp

    @classmethod
    def __post(cls, **kwargs):
        resp = requests.post(**kwargs)
        return resp

    @classmethod
    def __put(cls, **kwargs):
        resp = requests.put(**kwargs)
        # resp.raise_for_status()
        return resp

    @classmethod
    def __del(cls, **kwargs):
        resp = requests.delete(**kwargs)
        # resp.raise_for_status()
        return resp
