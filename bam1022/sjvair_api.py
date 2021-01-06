import json
import os

import requests


class Requestor:
    def __init__(self):
        self.session = self.make_session()

    def make_session(self):
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"Accept": "application/json"})
        return session

    def request(self, url, method=None, **kwargs):
        method = method or "get"

        response = self.session.request(method, url, **kwargs)
        response.is_success = lambda: response.ok
        response.is_error = lambda: not response.ok

        try:
            response.body = response.json()
        except Exception:
            response.body = None

        return response


class SJVAirAPI:
    base_url = os.environ.get('SJVAIR_URL', 'https://www.sjvair.com/api/1.0')
    monitor_id = os.environ.get('SJVAIR_MONITOR_ID')
    access_key = os.environ.get('SJVAIR_MONITOR_ACCESS_KEY')

    def __init__(self):
        self.requestor = Requestor()

    def request(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}/"
        return self.requestor.request(url, **kwargs)

    def add_entry(self, payload):
        endpoint = f'monitors/{self.monitor_id}/entries'
        return self.request(endpoint, method='post', json=payload, headers={
            'Access-Key': self.access_key,
        })

sjvair = SJVAirAPI()
