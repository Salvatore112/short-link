import secrets
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import URL, Visit


def generate_short_code(length: int = 6) -> str:
    return secrets.token_urlsafe(length)[:length]


def create_short_url(db: Session, url_data: dict, user_id: int):
    if url_data.get("custom_code"):
        short_code = url_data["custom_code"]
        existing_url = db.query(URL).filter(URL.short_code == short_code).first()
        if existing_url:
            raise HTTPException(status_code=400, detail="Custom code already in use")
    else:
        short_code = generate_short_code()

    expires_at = datetime.utcnow() + timedelta(days=url_data.get("expire_days", 1))

    db_url = URL(
        original_url=url_data["original_url"],
        short_code=short_code,
        expires_at=expires_at,
        user_id=user_id,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def record_visit(db: Session, url_id: int, client_ip: str = None):
    visit = Visit(url_id=url_id, client_ip=client_ip)
    db.add(visit)
    db.commit()
    return visit
