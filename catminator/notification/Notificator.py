import json

import requests
from requests.auth import HTTPBasicAuth

from config.config_file import ConfigFile


class Notificator:
    def __init__(self):
        config = ConfigFile("global.yml").load()
        self.url = config['push_bullet']['url']
        self.api_key = config['push_bullet']['api_key']

    def push_note(self, title: str, body: str):
        """
        Test example from terminal:
        curl -X POST "https://api.pushbullet.com/v2/pushes"
            -H "Access-Token: <token>" -H "Content-Type: application/json"
            --data-binary '{"body":"This is the body","title":"Interesting title","type":"note"}'
        """
        data = {"type": "note", "title": title, "body": body}
        return self._request("POST", self.url + "/pushes", data)

    def _request(self, method, url, post_data=None, params=None, files=None):
        headers = {"Content-Type": "application/json",
                   "Access-Token": self.api_key}

        if post_data:
            post_data = json.dumps(post_data)

        r = requests.request(method,
                             url,
                             data=post_data,
                             params=params,
                             headers=headers,
                             files=files,
                             auth=HTTPBasicAuth(self.api_key, ""))
        r.raise_for_status()
        return r.json()
