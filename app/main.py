from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from . import schemas, models
from .dependencies import get_db, get_current_user
from .services.url_service import create_short_url, record_visit
from .config import BASE_URL

app = FastAPI()


@app.post("/urls/", response_model=schemas.URLInfo)
def create_url(
    url: schemas.URLCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    db_url = create_short_url(db, url.dict(), user.id)
    return {
        "original_url": db_url.original_url,
        "short_url": f"{BASE_URL}/{db_url.short_code}",
        "is_active": db_url.is_active,
        "created_at": db_url.created_at,
        "expires_at": db_url.expires_at,
    }


@app.get("/urls/", response_model=List[schemas.URLInfo])
def list_urls(
    active_only: bool = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    query = db.query(models.URL).filter(models.URL.user_id == user.id)
    if active_only:
        query = query.filter(models.URL.is_active == True).filter(
            models.URL.expires_at > datetime.utcnow()
        )

    urls = query.offset(skip).limit(limit).all()
    return [
        {
            "original_url": url.original_url,
            "short_url": f"{BASE_URL}/{url.short_code}",
            "is_active": url.is_active,
            "created_at": url.created_at,
            "expires_at": url.expires_at,
        }
        for url in urls
    ]


@app.post("/urls/{short_code}/deactivate")
def deactivate_url(
    short_code: str,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    url = (
        db.query(models.URL)
        .filter(models.URL.short_code == short_code, models.URL.user_id == user.id)
        .first()
    )
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    url.is_active = False
    db.commit()
    return {"message": "URL deactivated successfully"}


@app.get("/stats/", response_model=List[schemas.URLStats])
def get_stats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    urls = (
        db.query(models.URL)
        .filter(models.URL.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    stats = []
    for url in urls:
        visit_count = (
            db.query(models.Visit).filter(models.Visit.url_id == url.id).count()
        )
        stats.append(
            {
                "short_url": f"{BASE_URL}/{url.short_code}",
                "original_url": url.original_url,
                "visits": visit_count,
            }
        )
    stats.sort(key=lambda x: x["visits"], reverse=True)
    return stats


@app.get("/{short_code}")
def redirect_url(
    short_code: str, db: Session = Depends(get_db), client_ip: Optional[str] = None
):
    url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not url or not url.is_active or url.expires_at < datetime.utcnow():
        raise HTTPException(status_code=404, detail="URL not found or expired")
    record_visit(db, url.id, client_ip)
    return RedirectResponse(url.original_url)
