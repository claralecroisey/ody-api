from base64 import b64encode

from app.models.user import User


class TestAuthRoutes:
    def test_call_auth_endpoint_without_authentication_returns_401(self, client):
        payload_body = {"user_id": "mocked_user_id"}
        response = client.post("/auth", json=payload_body)

        assert response.status_code == 401

    def test_create_user_from_payload_if_new_user(self, client):
        payload_body = {"user_id": "sub|new_user_id"}
        assert User.query.get("new_user_id") is None  # User does not exist yet

        # Basic auth header with test credentials
        credentials = b64encode(b"username:password").decode("utf-8")
        headers = {"Authorization": f"Basic {credentials}"}

        response = client.post("/auth", json=payload_body, headers=headers)

        assert User.query.get("new_user_id") is not None
        assert response.status_code == 200

    def test_do_not_create_user_from_payload_if_user_already_exists(self, client):
        payload_body = {"user_id": "sub|mocked_user_id"}
        # User already exists (see setup_default_user fixture)
        assert User.query.get("mocked_user_id") is not None

        # Basic auth header with test credentials
        credentials = b64encode(b"username:password").decode("utf-8")
        headers = {"Authorization": f"Basic {credentials}"}

        response = client.post("/auth", json=payload_body, headers=headers)

        assert response.status_code == 200
