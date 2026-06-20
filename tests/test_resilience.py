"""
Resilience tests: SLA assertions under delayed responses and negative-path
parametrization. These validate that the suite itself handles adverse
conditions correctly, not just the happy path.
"""
import pytest

from fixtures import EXISTING_USER_ID

# reqres.in supports ?delay=N (seconds) to simulate slow backends
DELAY_SECONDS = 3
SLA_BUFFER_MS = 1500  # allowed headroom on top of the introduced delay


@pytest.mark.slow
class TestDelayedResponses:
    def test_list_users_within_sla_under_delay(self, users_client):
        response = users_client.get(
            "/api/users", params={"page": 1, "delay": DELAY_SECONDS}
        )
        assert response.status_code == 200
        elapsed_ms = response.elapsed.total_seconds() * 1000
        max_allowed = (DELAY_SECONDS * 1000) + SLA_BUFFER_MS
        assert elapsed_ms <= max_allowed, (
            f"Response exceeded SLA: {elapsed_ms:.0f}ms (limit {max_allowed}ms)"
        )

    def test_get_user_within_sla_under_delay(self, users_client):
        response = users_client.get(
            f"/api/users/{EXISTING_USER_ID}", params={"delay": DELAY_SECONDS}
        )
        assert response.status_code == 200
        elapsed_ms = response.elapsed.total_seconds() * 1000
        max_allowed = (DELAY_SECONDS * 1000) + SLA_BUFFER_MS
        assert elapsed_ms <= max_allowed, (
            f"Response exceeded SLA: {elapsed_ms:.0f}ms (limit {max_allowed}ms)"
        )

    def test_delayed_response_still_returns_valid_data(self, users_client):
        response = users_client.get(
            "/api/users", params={"page": 1, "delay": 1}
        )
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert len(body["data"]) > 0


@pytest.mark.auth
class TestLoginNegativeCases:
    @pytest.mark.parametrize("email,password,expected_status", [
        ("",                    "password",    400),   # empty email
        ("not-an-email",        "password",    400),   # malformed email
        ("peter@klaven@reqres", "cityslicka",  400),   # unregistered
    ])
    def test_login_invalid_inputs_return_4xx(self, auth_client, email, password, expected_status):
        response = auth_client.login(email, password)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("payload,description", [
        ({"email": "eve.holt@reqres.in"},               "missing password field"),
        ({"password": "cityslicka"},                     "missing email field"),
        ({},                                             "completely empty body"),
        ({"email": None, "password": "cityslicka"},     "null email"),
    ])
    def test_login_malformed_payloads_return_400(self, auth_client, payload, description):
        response = auth_client.post("/api/login", json=payload)
        assert response.status_code == 400, f"Expected 400 for: {description}"


@pytest.mark.users
class TestUserEdgeCases:
    @pytest.mark.parametrize("user_id,expected_status", [
        (0,     404),   # zero ID
        (-1,    404),   # negative ID
        (9999,  404),   # far out of range
    ])
    def test_get_invalid_user_ids_return_404(self, users_client, user_id, expected_status):
        response = users_client.get_user(user_id)
        assert response.status_code == expected_status

    @pytest.mark.parametrize("name,job", [
        ("",        "engineer"),    # empty name
        ("morpheus", ""),           # empty job
        ("a" * 255, "b" * 255),    # max-length strings
        ("Neo <script>", "hacker"), # special characters
    ])
    def test_create_user_with_edge_case_inputs(self, users_client, name, job):
        response = users_client.create_user(name, job)
        # reqres accepts any string — assert it echoes back what we sent
        assert response.status_code == 201
        assert response.json()["name"] == name
        assert response.json()["job"] == job
