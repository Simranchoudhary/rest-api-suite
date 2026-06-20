import pytest

from fixtures import EXISTING_USER_ID, NEW_USER, VALID_CREDS


@pytest.mark.headers
class TestResponseHeaders:
    """Assert that all JSON endpoints return the correct Content-Type header."""

    def test_list_users_content_type(self, users_client):
        response = users_client.list_users()
        assert "application/json" in response.headers.get("Content-Type", "")

    def test_get_user_content_type(self, users_client):
        response = users_client.get_user(EXISTING_USER_ID)
        assert "application/json" in response.headers.get("Content-Type", "")

    def test_create_user_content_type(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert "application/json" in response.headers.get("Content-Type", "")

    def test_login_content_type(self, auth_client):
        response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        assert "application/json" in response.headers.get("Content-Type", "")

    def test_responses_include_content_type_header(self, users_client):
        response = users_client.list_users()
        assert "Content-Type" in response.headers
