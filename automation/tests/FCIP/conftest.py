from common.FCIP_token import Token
import pytest


# 获取FCIP_token,作用范围session
@pytest.fixture(scope='session', autouse=True)
def token():
    headers = {
        'authorization': 'Bearer ' + Token().get_token()
    }
    return headers
