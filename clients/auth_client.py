from requests import Response

from .base_client import BaseClient


class AuthClient(BaseClient):
    def login(self, email: str, password: str) -> Response:
        return self.post("/api/login", json={"email": email, "password": password})

    def register(self, email: str, password: str) -> Response:
        return self.post("/api/register", json={"email": email, "password": password})

    def login_missing_password(self, email: str) -> Response:
        return self.post("/api/login", json={"email": email})

    def register_missing_password(self, email: str) -> Response:
        return self.post("/api/register", json={"email": email})
