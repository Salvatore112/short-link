from fastapi import status
from datetime import datetime, timedelta


def test_create_url(client, test_user):
    auth = (test_user.username, "testpass")
    response = client.post(
        "/urls/",
        json={"original_url": "https://example.com", "expire_days": 1},
        auth=auth,
    )
    assert response.status_code == status.HTTP_200_OK
    assert "short_url" in response.json()


def test_list_urls(client, test_user, test_url):
    auth = (test_user.username, "testpass")
    response = client.get("/urls/", auth=auth)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["original_url"] == "https://example.com"


def test_deactivate_url(client, test_user, test_url):
    auth = (test_user.username, "testpass")
    response = client.post(f"/urls/{test_url.short_code}/deactivate", auth=auth)
    assert response.status_code == 200
    assert response.json() == {"message": "URL deactivated successfully"}
