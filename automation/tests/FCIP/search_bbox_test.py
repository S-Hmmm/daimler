from common.client import Client
from data.read_data import yaml_data_load
from common.utils import parametrize, all_true
import pytest
import allure

method, url, cases, parameters = yaml_data_load('search_bbox.yaml')
req = Client().req(method)


@allure.story('MFS根据vin获取FCI信息')
@allure.description('无')
@pytest.mark.search_bbox
@parametrize(parameters, cases)
def test_bbox(http, expected, token):
    http['headers'].update(token)
    resp = req(url=url, **http)
    allure.attach(str(resp.status_code).encode('utf-8'), name='status_code')
    allure.attach(resp.content, name='Response')  # allure add comment
    resp_j = resp.json()

    # assert
    if expected.get('status'):
        assert resp.status_code < 400
        if not resp_j:
            assert resp_j == expected['result']
        else:
            for fci in resp_j:
                if http['params'].get('namespace') and http['params'].get('fields'):
                    assert fci['namespace'] == http['params']['namespace']
                assert len(fci['gpsTrail']) >= 2
                assert any(
                    http['params']['minLon'] <= gps['lon'] <= http['params']['maxLon'] and
                    http['params']['minLat'] <= gps['lat'] <= http['params']['maxLat']
                    for gps in fci['gpsTrail']
                )
                if expected.get('tsh'):
                    assert any(all_true(matcher[k] == expected['tsh'][k] or matcher[k] is None for k in matcher.keys())
                               for matcher in fci['matchers'])
    else:
        assert not resp_j or resp.status_code >= 400
