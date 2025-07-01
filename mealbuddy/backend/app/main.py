from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.base import get_db
from app.schemas.token import Token, UserCreate, UserInDB
from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from datetime import timedelta

app = FastAPI(
    title="MealBuddy API",
    description="API for MealBuddy - AI-Powered Meal Planning",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to MealBuddy API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Root endpoint for OpenAPI schema
@app.get("/openapi.json")
async def get_openapi_schema():
    return app.openapi()
