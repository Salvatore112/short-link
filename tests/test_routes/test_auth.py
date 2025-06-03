from fastapi import status
from fastapi.security import HTTPBasicCredentials


def test_successful_auth(client, test_user):
    """Test successful authentication"""
    credentials = HTTPBasicCredentials(
        username=test_user.username,
        password="testpass",  # From test_user fixture
    )
    response = client.get("/urls/", auth=(test_user.username, "testpass"))
    assert response.status_code == status.HTTP_200_OK


def test_failed_auth_wrong_password(client, test_user):
    """Test authentication fails with wrong password"""
    response = client.get("/urls/", auth=(test_user.username, "wrongpass"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect username or password" in response.text


def test_failed_auth_unknown_user(client):
    """Test authentication fails with unknown user"""
    response = client.get("/urls/", auth=("nonexistent", "password"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_protected_routes_require_auth(client):
    """Verify protected routes require authentication"""
    protected_routes = [
        ("GET", "/urls/"),
        ("POST", "/urls/"),
        ("POST", "/urls/abc123/deactivate"),
        ("GET", "/stats/"),
    ]

    for method, route in protected_routes:
        if method == "GET":
            response = client.get(route)
        elif method == "POST":
            response = client.post(route)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
