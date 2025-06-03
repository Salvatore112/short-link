from fastapi import FastAPI
from .config import engine
from . import models

app = FastAPI(
    title="URL Alias Service",
    description="Service for creating short aliases for long URLs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

models.Base.metadata.create_all(bind=engine)
