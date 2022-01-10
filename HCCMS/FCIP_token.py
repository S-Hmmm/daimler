from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

client_id = 'DAIVBADM_MICTM_CN_NONPROD_00371'
token_url = 'https://ssoalpha.dvb.corpinter.net.cn/v1/token'
client_secret = 'c54Us1GL~el8o206u9f.FwyI7PW-_Sv3'
scope = ['openid', 'groups', 'audience:server:client_id:DAIVBADM_MICTM_CN_NONPROD_00441']


class Token(OAuth2Session):

    def __init__(self):
        super().__init__(client=BackendApplicationClient(client_id))

    def get_token(self):
        auth = HTTPBasicAuth(client_id, client_secret)
        token = self.fetch_token(token_url=token_url, auth=auth, scope=scope)['access_token']
        if token:
            return token
        else:
            return None
