from urllib import parse

from common.client import req
from data.read_data import yaml_load_ls
from common.utils import parametrize_ls
import pytest
import allure


method, url, cases, parameters = yaml_load_ls('FCIP/del_fapconfigitems.yaml')


@allure.story('删除FCI')
@allure.description('无')
@pytest.mark.del_item
@parametrize_ls(parameters, cases)
def test_get_fapconfigitems(http, expected, item_id, token):
    http['headers'].update(token)
    http['url'] = parse.urljoin(url, str(item_id))
    resp = req(method, **http)
    allure.attach(str(resp.status_code).encode('utf-8'), name='status_code')
    allure.attach(str(resp.headers).encode('utf-8'), name='headers', attachment_type=allure.attachment_type.TEXT)
    if resp.content:
        allure.attach(resp.content, name='resp_body')
    # assert
    if expected.get('status'):
        assert resp.status_code == 200, resp.url
        assert req('get', **http).json()['error-message'] in 'fapConfigItem could not be found'
    else:
        assert resp.status_code >= 400, resp.url
