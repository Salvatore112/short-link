from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class URLBase(BaseModel):
    original_url: str
    custom_code: Optional[str] = None
    expire_days: Optional[int] = 1


class URLCreate(URLBase):
    pass


class URLInfo(URLBase):
    short_url: str
    is_active: bool
    created_at: datetime
    expires_at: datetime


class URLStats(BaseModel):
    short_url: str
    original_url: str
    visits: int
