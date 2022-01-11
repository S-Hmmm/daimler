import requests


def req(method, **kwargs):
    if str.upper(str(method)) not in ['GET', 'POST', 'PUT', 'DELETE', 'OPTION', 'HEAD', 'PATCH']:
        raise ValueError('method must in GET, POST, PUT, DELETE, OPTION, HEAD, PATCH')
    return requests.request(method=method, **kwargs)
