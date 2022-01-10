from common.client import Client
from data.read_data import yaml_data_load
from common.utils import parametrize, utc_time
from common.logger import get_logger
import pytest
import allure
from urllib import parse

log = get_logger()
method, url, cases, parameters = yaml_data_load('update_fapconfigitems.yaml')
req = Client().req(method)
utc_now = utc_time()


@allure.story('更新FCI')
@allure.description('无')
@pytest.mark.update_item
@parametrize(parameters, cases)
def test_get_fapconfigitems(http, expected, token):
    http['headers'].update(token)
    http['url'] = parse.urljoin(url, str(http['url']))
    resp = req(**http)
    allure.attach(resp.content, name='Response')  # allure add comment
    resp_j = resp.json()
    log.info(resp_j)
    # assert
    if expected.get('status'):
        for k in http['json'].keys():
            assert resp_j[k] == http['json'][k]
        assert resp_j['modificationDate'] > utc_now
    else:
        assert resp.status_code >= 400
