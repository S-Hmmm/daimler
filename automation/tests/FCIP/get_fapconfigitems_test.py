from common.client import req
from data.read_data import yaml_load_ls
from common.utils import parametrize_ls
import pytest
import allure
from urllib import parse

method, url, cases, parameters = yaml_load_ls('FCIP/get_fapconfigitems.yaml')


@allure.story('查询FCI信息')
@allure.description('无')
@pytest.mark.get_item
@parametrize_ls(parameters, cases)
def test_get_fapconfigitems(http, expected, item_id, token):
    http['headers'].update(token)
    http['url'] = parse.urljoin(url, str(item_id))
    resp = req(method, **http)
    allure.attach(str(resp.status_code).encode('utf-8'), name='status_code')
    allure.attach(str(resp.headers).encode('utf-8'), name='header')
    if resp.content:
        allure.attach(resp.content, name='body')  # allure add comment
    resp_j = resp.json()
    # assert
    if expected.get('status'):
        assert resp_j.get('id'), "Can't find id: " + resp.url
        assert int(resp_j['id']) == int(item_id), resp.url
    else:
        assert resp.status_code >= 400, resp.url
