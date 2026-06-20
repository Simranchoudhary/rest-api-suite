import pytest

from fixtures import REGISTER_CREDS, UNREGISTERED_USER, VALID_CREDS
from utils import assert_response_time, validate_schema


@pytest.mark.auth
class TestLogin:
    def test_successful_login_returns_200(self, auth_client):
        response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        assert response.status_code == 200

    def test_successful_login_returns_token(self, auth_client):
        response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        body = response.json()
        assert "token" in body
        assert isinstance(body["token"], str)
        assert len(body["token"]) > 0

    def test_login_response_conforms_to_schema(self, auth_client):
        response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        validate_schema(response.json(), "auth_login")

    def test_login_response_time(self, auth_client):
        response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        assert_response_time(response, max_ms=3000)

    def test_login_missing_password_returns_400(self, auth_client):
        response = auth_client.login_missing_password(VALID_CREDS.email)
        assert response.status_code == 400

    def test_login_missing_password_returns_error_message(self, auth_client):
        response = auth_client.login_missing_password(VALID_CREDS.email)
        assert "error" in response.json()
        assert response.json()["error"] == "Missing password"

    def test_login_unregistered_user_returns_400(self, auth_client):
        response = auth_client.login(UNREGISTERED_USER.email, "anypassword")
        assert response.status_code == 400

    def test_login_unregistered_user_returns_error_message(self, auth_client):
        response = auth_client.login(UNREGISTERED_USER.email, "anypassword")
        assert "error" in response.json()

    def test_login_empty_body_returns_400(self, auth_client):
        response = auth_client.post("/api/login", json={})
        assert response.status_code == 400

    def test_consecutive_logins_return_same_token(self, auth_client):
        r1 = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        r2 = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        assert r1.json()["token"] == r2.json()["token"]


@pytest.mark.auth
class TestRegister:
    def test_successful_register_returns_200(self, auth_client):
        response = auth_client.register(REGISTER_CREDS.email, REGISTER_CREDS.password)
        assert response.status_code == 200

    def test_successful_register_returns_id_and_token(self, auth_client):
        response = auth_client.register(REGISTER_CREDS.email, REGISTER_CREDS.password)
        body = response.json()
        assert "id" in body
        assert "token" in body

    def test_register_response_conforms_to_schema(self, auth_client):
        response = auth_client.register(REGISTER_CREDS.email, REGISTER_CREDS.password)
        validate_schema(response.json(), "auth_register")

    def test_register_missing_password_returns_400(self, auth_client):
        response = auth_client.register_missing_password(REGISTER_CREDS.email)
        assert response.status_code == 400

    def test_register_missing_password_returns_error(self, auth_client):
        response = auth_client.register_missing_password(REGISTER_CREDS.email)
        assert response.json().get("error") == "Missing password"

    def test_register_unregistered_email_returns_400(self, auth_client):
        response = auth_client.register(UNREGISTERED_USER.email, "password123")
        assert response.status_code == 400

    def test_register_unregistered_email_returns_error(self, auth_client):
        response = auth_client.register(UNREGISTERED_USER.email, "password123")
        assert "error" in response.json()
        assert "defined" in response.json()["error"].lower()
