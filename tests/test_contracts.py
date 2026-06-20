"""
Contract tests: every API response must match its registered schema.
These run independently of functional assertions — a contract test failure
means the API changed shape, not just behaviour.
"""
import pytest
from clients import AuthClient, UsersClient
from fixtures import VALID_CREDS, REGISTER_CREDS, EXISTING_USER_ID, NEW_USER
from utils import validate_schema


@pytest.mark.contract
class TestAuthContracts:
    def test_login_success_contract(self, auth_client):
        response = auth_client.login(VALID_CREDS.email, VALID_CREDS.password)
        assert response.status_code == 200
        validate_schema(response.json(), "auth_login")

    def test_register_success_contract(self, auth_client):
        response = auth_client.register(REGISTER_CREDS.email, REGISTER_CREDS.password)
        assert response.status_code == 200
        validate_schema(response.json(), "auth_register")


@pytest.mark.contract
class TestUsersContracts:
    def test_list_users_contract(self, users_client):
        response = users_client.list_users()
        assert response.status_code == 200
        validate_schema(response.json(), "users_list")

    def test_get_single_user_contract(self, users_client):
        response = users_client.get_user(EXISTING_USER_ID)
        assert response.status_code == 200
        validate_schema(response.json(), "user")

    def test_create_user_contract(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert response.status_code == 201
        validate_schema(response.json(), "created_user")

    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5, 6])
    def test_all_listed_users_match_schema(self, users_client, user_id):
        response = users_client.get_user(user_id)
        assert response.status_code == 200
        validate_schema(response.json(), "user")
