from datetime import datetime, timedelta
import pytest
from app.services.url_service import create_short_url, record_visit
from fastapi import HTTPException


def test_create_short_url(db, test_user):
    url_data = {
        "original_url": "https://example.com",
        "custom_code": None,
        "expire_days": 1,
    }
    url = create_short_url(db, url_data, test_user.id)
    assert url.original_url == "https://example.com"
    assert len(url.short_code) == 6
    assert url.is_active is True
    assert url.user_id == test_user.id


def test_create_short_url_with_custom_code(db, test_user):
    url_data = {
        "original_url": "https://example.com",
        "custom_code": "custom",
        "expire_days": 1,
    }
    url = create_short_url(db, url_data, test_user.id)
    assert url.short_code == "custom"


def test_create_short_url_duplicate_code(db, test_user):
    url_data = {
        "original_url": "https://example.com",
        "custom_code": "duplicate",
        "expire_days": 1,
    }
    create_short_url(db, url_data, test_user.id)

    with pytest.raises(HTTPException):
        create_short_url(db, url_data, test_user.id)


def test_record_visit(db, test_url):
    visit = record_visit(db, test_url.id, "127.0.0.1")
    assert visit.url_id == test_url.id
    assert visit.client_ip == "127.0.0.1"
