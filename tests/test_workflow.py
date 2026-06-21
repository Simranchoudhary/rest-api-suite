import time

import pytest

from fixtures import NEW_USER, UPDATED_USER

# reqres.in free tier rate-limits ~30 req/min; a short pause keeps workflows
# from hitting 429 when the full suite runs back-to-back in CI.
_RATE_LIMIT_PAUSE = 2


@pytest.mark.workflow
class TestCRUDWorkflow:
    """End-to-end create → update → delete lifecycle in a single chained flow."""

    def test_full_user_lifecycle(self, users_client):
        time.sleep(_RATE_LIMIT_PAUSE)
        create = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert create.status_code == 201, (
            f"Create failed — got {create.status_code}. "
            "429 means rate-limited; increase _RATE_LIMIT_PAUSE."
        )
        user_id = int(create.json()["id"])

        update = users_client.update_user(user_id, UPDATED_USER.name, UPDATED_USER.job)
        assert update.status_code == 200
        assert update.json()["name"] == UPDATED_USER.name
        assert update.json()["job"] == UPDATED_USER.job
        assert "updatedAt" in update.json()

        delete = users_client.delete_user(user_id)
        assert delete.status_code == 204

    def test_patch_then_delete(self, users_client):
        time.sleep(_RATE_LIMIT_PAUSE)
        create = users_client.create_user(NEW_USER.name, NEW_USER.job)
        assert create.status_code == 201, (
            f"Create failed — got {create.status_code}. "
            "429 means rate-limited; increase _RATE_LIMIT_PAUSE."
        )
        user_id = int(create.json()["id"])

        patch = users_client.patch_user(user_id, job=UPDATED_USER.job)
        assert patch.status_code == 200
        assert patch.json()["job"] == UPDATED_USER.job

        delete = users_client.delete_user(user_id)
        assert delete.status_code == 204
