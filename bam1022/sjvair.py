import json

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
    domain = "www.sjvair.com"

    def __init__(self, monitor_id):
        self.monitor_id = monitor_id
        self.requestor = Requestor(self)

    def request(self, path, **kwargs):
        url = f"https://{self.domain}/api/1.0/{path}/"
        return self.requestor.request(url, **kwargs)

    def add_entry(self, payload):
        path = f'monitors/{self.monitor_id}/entries'
        return self.request(path, method='post', data=data)
