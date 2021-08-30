import requests as rq

class BearerAuth(rq.auth.AuthBase):
    def __init__(self, token):
        self.token = token
        
    def __call__(self, r):
        r.headers['authorization'] = f'Bearer {self.token}'
        return r


def get_tws(url):
    bearer = open('key.txt', 'r').read().split('\n')[0]
    data = rq.get(url, auth=BearerAuth(bearer))

    if data.status_code == 200:
        data = data.json()
        return data

    return 'error'
