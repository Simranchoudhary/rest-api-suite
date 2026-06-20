import pytest

from fixtures import (
    EXISTING_USER_ID,
    INVALID_PAGE,
    NEW_USER,
    NON_EXISTENT_USER_ID,
    UPDATED_USER,
    VALID_PAGE,
)
from utils import assert_response_time, validate_schema


@pytest.mark.users
class TestListUsers:
    def test_list_users_returns_200(self, users_client):
        response = users_client.list_users()
        assert response.status_code == 200

    def test_list_users_response_conforms_to_schema(self, users_client):
        response = users_client.list_users()
        validate_schema(response.json(), "users_list")

    def test_list_users_default_page_is_1(self, users_client):
        response = users_client.list_users()
        assert response.json()["page"] == 1

    def test_list_users_returns_correct_page(self, users_client):
        response = users_client.list_users(page=2)
        assert response.json()["page"] == 2

    def test_list_users_data_not_empty_on_valid_page(self, users_client):
        response = users_client.list_users(page=VALID_PAGE)
        assert len(response.json()["data"]) > 0

    def test_list_users_data_empty_on_nonexistent_page(self, users_client):
        response = users_client.list_users(page=INVALID_PAGE)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_list_users_pagination_totals_are_consistent(self, users_client):
        response = users_client.list_users()
        body = response.json()
        assert body["total"] >= body["total_pages"] * 1
        assert body["total_pages"] == -(-body["total"] // body["per_page"])

    def test_list_users_response_time(self, users_client):
        response = users_client.list_users()
        assert_response_time(response, max_ms=3000)

    def test_list_users_each_item_has_required_fields(self, users_client):
        response = users_client.list_users()
        for user in response.json()["data"]:
            assert "id" in user
            assert "email" in user
            assert "@" in user["email"]


@pytest.mark.users
class TestGetUser:
    def test_get_existing_user_returns_200(self, users_client):
        response = users_client.get_user(EXISTING_USER_ID)
        assert response.status_code == 200

    def test_get_user_response_conforms_to_schema(self, users_client):
        response = users_client.get_user(EXISTING_USER_ID)
        validate_schema(response.json(), "user")

    def test_get_user_id_matches_requested(self, users_client):
        response = users_client.get_user(EXISTING_USER_ID)
        assert response.json()["data"]["id"] == EXISTING_USER_ID

    def test_get_nonexistent_user_returns_404(self, users_client):
        response = users_client.get_user(NON_EXISTENT_USER_ID)
        assert response.status_code == 404

    def test_get_nonexistent_user_returns_empty_body(self, users_client):
        response = users_client.get_user(NON_EXISTENT_USER_ID)
        assert response.json() == {}

    def test_get_user_response_time(self, users_client):
        response = users_client.get_user(EXISTING_USER_ID)
        assert_response_time(response, max_ms=3000)


@pytest.mark.users
class TestCreateUser:
    def test_create_user_returns_201(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert response.status_code == 201

    def test_create_user_response_conforms_to_schema(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        validate_schema(response.json(), "created_user")

    def test_create_user_name_matches_input(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert response.json()["name"] == NEW_USER.name

    def test_create_user_job_matches_input(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert response.json()["job"] == NEW_USER.job

    def test_create_user_returns_id(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert "id" in response.json()

    def test_create_user_returns_created_at(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert "createdAt" in response.json()

    def test_create_user_response_time(self, users_client):
        response = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert_response_time(response, max_ms=3000)


@pytest.mark.users
class TestUpdateUser:
    def test_put_user_returns_200(self, users_client):
        response = users_client.update_user(EXISTING_USER_ID, UPDATED_USER.name, UPDATED_USER.job)
        assert response.status_code == 200

    def test_put_user_name_updated(self, users_client):
        response = users_client.update_user(EXISTING_USER_ID, UPDATED_USER.name, UPDATED_USER.job)
        assert response.json()["name"] == UPDATED_USER.name

    def test_put_user_job_updated(self, users_client):
        response = users_client.update_user(EXISTING_USER_ID, UPDATED_USER.name, UPDATED_USER.job)
        assert response.json()["job"] == UPDATED_USER.job

    def test_put_user_returns_updated_at(self, users_client):
        response = users_client.update_user(EXISTING_USER_ID, UPDATED_USER.name, UPDATED_USER.job)
        assert "updatedAt" in response.json()

    def test_patch_user_returns_200(self, users_client):
        response = users_client.patch_user(EXISTING_USER_ID, job="zion architect")
        assert response.status_code == 200

    def test_patch_user_only_updates_provided_field(self, users_client):
        new_job = "zion architect"
        response = users_client.patch_user(EXISTING_USER_ID, job=new_job)
        assert response.json()["job"] == new_job

    def test_patch_user_returns_updated_at(self, users_client):
        response = users_client.patch_user(EXISTING_USER_ID, job="any job")
        assert "updatedAt" in response.json()


@pytest.mark.users
class TestDeleteUser:
    def test_delete_user_returns_204(self, users_client):
        response = users_client.delete_user(EXISTING_USER_ID)
        assert response.status_code == 204

    def test_delete_user_returns_empty_body(self, users_client):
        response = users_client.delete_user(EXISTING_USER_ID)
        assert response.text == ""
