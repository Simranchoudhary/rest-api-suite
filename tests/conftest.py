import pytest

from clients import AuthClient, UsersClient
from fixtures import VALID_CREDS


@pytest.fixture(scope="session")
def auth_client():
    client = AuthClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def users_client():
    client = UsersClient()
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_token(auth_client):
    response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
    assert response.status_code == 200, "Failed to obtain auth token in session setup"
    return response.json()["token"]


@pytest.fixture(scope="session")
def authenticated_users_client(auth_token):
    client = UsersClient(token=auth_token)
    yield client
    client.close()
