from requests import Response
from .base_client import BaseClient


class UsersClient(BaseClient):
    def list_users(self, page: int = 1, per_page: int = 6) -> Response:
        return self.get("/api/users", params={"page": page, "per_page": per_page})

    def get_user(self, user_id: int) -> Response:
        return self.get(f"/api/users/{user_id}")

    def create_user(self, name: str, job: str) -> Response:
        return self.post("/api/users", json={"name": name, "job": job})

    def update_user(self, user_id: int, name: str, job: str) -> Response:
        return self.put(f"/api/users/{user_id}", json={"name": name, "job": job})

    def patch_user(self, user_id: int, **fields) -> Response:
        return self.patch(f"/api/users/{user_id}", json=fields)

    def delete_user(self, user_id: int) -> Response:
        return self.delete(f"/api/users/{user_id}")

    def get_unknown_resource(self, resource_id: int | None = None) -> Response:
        path = "/api/unknown" if resource_id is None else f"/api/unknown/{resource_id}"
        return self.get(path)
