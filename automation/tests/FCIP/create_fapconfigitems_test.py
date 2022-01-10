from common.logger import get_logger
from common.client import Client
from data.read_data import yaml_data_load
from common.utils import parametrize, utc_time
import pytest
import allure
import yaml

log = get_logger()
method, url, cases, parameters = yaml_data_load('create_fapconfigitems.yaml')
req = Client().req(method)
utc_now = utc_time()


@allure.story('创建FCI')
@allure.description('无')
@pytest.mark.create_item
@parametrize(parameters, cases)
def test_get_fapconfigitems(http, expected, token):
    http['headers'].update(token)
    resp = req(url=url, **http)
    allure.attach(str(resp.status_code).encode('utf-8'), name='status_code')
    allure.attach(str(resp.headers).encode('utf-8'), name='headers')
    if resp.content:
        allure.attach(resp.content, name='Response')  # allure add comment
    resp_j = resp.json()
    log.info(resp.json())
    if resp_j.get('id'):
        with open('data/items.yaml', 'a') as f:
            items = yaml.dump([resp_j['id']], Dumper=yaml.SafeDumper)
            f.write(items)
    # assert
    if expected.get('status'):
        assert 200 <= resp.status_code < 400
        # for k in http['json'].keys():
        #     assert resp_j[k] == http['json'][k]
        assert resp_j['id'] is not None
        assert resp_j['creationDate'] > utc_now
        assert resp_j['modificationDate'] > utc_now
    else:
        assert not resp_j.get('id')
