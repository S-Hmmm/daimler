import json
from urllib.parse import urljoin

import requests

from hccms_token import token

RT_URL = 'https://hccms-int.adbdaimlercn.com/rest/roadsegmentticket/'
TICKET_URL = 'https://hccms-int.adbdaimlercn.com/rest/validationticket/'
HEADER = {
    'content-type': 'application/json',
    'cookie': token,
    }
PUT_HEADER = {
    'content-type': 'text/plain',
    'cookie': token,
}


class RoadSegmentTicket:
    def __init__(self, tk_id=None):
        self.tk_id = tk_id

    def create_ticket(self, data):
        resp = requests.post(url=RT_URL, headers=HEADER, data=json.dumps(data), verify=False)
        resp.raise_for_status()
        if resp.status_code == 201:
            self.tk_id = str(resp.json()['key'])
        print(resp.json()['key'], resp.json()['status'])
        return resp.json()

    def request_validate_ticket(self):
        url = urljoin(RT_URL, str(self.tk_id) + '/status')
        data = 'REQUEST_VALIDATION'
        resp = requests.put(url=url, headers=PUT_HEADER, data=data, verify=False)
        resp.raise_for_status()
        # print(resp.json())
        print(self.tk_id, resp.json()['status'])
        return resp.json()

    def approve_all_vl_tk(self):
        vl_tk_url = urljoin(RT_URL, str(self.tk_id) + '/validation')
        vl_tk_res = requests.get(vl_tk_url, headers=HEADER, verify=False).json()
        vl_tk_ls = []
        for item in vl_tk_res['validationTickets']:
            vl_tk_ls.append(item['key'])

        for vl_tk in vl_tk_ls:
            url = urljoin(TICKET_URL, str(vl_tk) + '/status')
            data = 'VALIDATED'
            resp = requests.put(url, headers=PUT_HEADER, data=data, verify=False)
            # print(resp.json())
            print(vl_tk, resp.json()['status'])
            return resp.json()

    def validate_ticket(self):
        url = urljoin(RT_URL, str(self.tk_id) + '/status')
        data = 'VALIDATED'
        resp = requests.put(url=url, headers=PUT_HEADER, data=data, verify=False)
        resp.raise_for_status()
        print(self.tk_id, resp.json()['status'])
        return resp.json()

    def release_ticket(self):
        url = urljoin(RT_URL, str(self.tk_id) + '/status')
        data = 'RELEASED'
        resp = requests.put(url=url, headers=PUT_HEADER, data=data, verify=False)
        resp.raise_for_status()
        print(self.tk_id, resp.json()['status'])
        return resp.json()

    @classmethod
    def del_rt_ticket(cls, tk_id):
        url = urljoin(RT_URL, str(tk_id))
        resp = requests.delete(url=url, headers=HEADER, verify=False)
        print(resp.status_code)
        return resp
