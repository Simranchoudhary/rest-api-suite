import os

import requests
from requests import Response

from config.settings import get_env


class BaseClient:
    def __init__(self, token: str | None = None):
        env = get_env()
        self.base_url = env.base_url
        self.timeout = env.timeout
        self.verify_ssl = env.verify_ssl
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        api_key = os.getenv("REQRES_API_KEY")
        if api_key:
            self.session.headers.update({"x-api-key": api_key})

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, path: str, **kwargs) -> Response:
        return self.session.get(
            f"{self.base_url}{path}", timeout=self.timeout, verify=self.verify_ssl, **kwargs
        )

    def post(self, path: str, **kwargs) -> Response:
        return self.session.post(
            f"{self.base_url}{path}", timeout=self.timeout, verify=self.verify_ssl, **kwargs
        )

    def put(self, path: str, **kwargs) -> Response:
        return self.session.put(
            f"{self.base_url}{path}", timeout=self.timeout, verify=self.verify_ssl, **kwargs
        )

    def patch(self, path: str, **kwargs) -> Response:
        return self.session.patch(
            f"{self.base_url}{path}", timeout=self.timeout, verify=self.verify_ssl, **kwargs
        )

    def delete(self, path: str, **kwargs) -> Response:
        return self.session.delete(
            f"{self.base_url}{path}", timeout=self.timeout, verify=self.verify_ssl, **kwargs
        )

    def close(self):
        self.session.close()
