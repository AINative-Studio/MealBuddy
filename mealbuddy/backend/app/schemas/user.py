from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, EmailStr, Field, validator, root_validator

from app.models.user import Gender, ActivityLevel, Goal


class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(UserBase):
    """Schema for creating a new user (registration)"""
    password: str = Field(..., min_length=8, max_length=100)
    password_confirm: str

    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = Field(None, gt=0, le=300)  # Reasonable height range
    weight_kg: Optional[float] = Field(None, gt=0, le=500)  # Reasonable weight range
    activity_level: Optional[ActivityLevel] = None
    goal: Optional[Goal] = None


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user dietary preferences"""
    dietary_restrictions: Optional[Dict[str, bool]] = {}
    allergies: Optional[List[str]] = []
    disliked_ingredients: Optional[List[str]] = []
    preferred_cuisines: Optional[List[str]] = []
    weekly_budget_cents: Optional[int] = Field(None, ge=0)


class UserNutritionUpdate(BaseModel):
    """Schema for updating user nutrition goals"""
    target_daily_calories: Optional[int] = Field(None, gt=0)
    target_protein_g: Optional[int] = Field(None, ge=0)
    target_carbs_g: Optional[int] = Field(None, ge=0)
    target_fats_g: Optional[int] = Field(None, ge=0)


class UserInDBBase(UserBase):
    """Base schema for user in database"""
    id: int
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[ActivityLevel] = None
    goal: Optional[Goal] = None
    dietary_restrictions: Dict[str, bool] = {}
    allergies: List[str] = []
    disliked_ingredients: List[str] = []
    preferred_cuisines: List[str] = []
    weekly_budget_cents: Optional[int] = None
    target_daily_calories: Optional[int] = None
    target_protein_g: Optional[int] = None
    target_carbs_g: Optional[int] = None
    target_fats_g: Optional[int] = None
    pantry_inventory: List[Dict[str, str]] = []
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    login_count: int = 0

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """Schema for returning user data (excludes sensitive info)"""
    pass


class UserInDB(UserInDBBase):
    """Schema for user in database (includes hashed password)"""
    hashed_password: str


class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""
    email: Optional[str] = None
    scopes: List[str] = []


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserRegister(UserCreate):
    """Schema for user registration"""
    pass


class UserInventoryUpdate(BaseModel):
    """Schema for updating user inventory"""
    pantry_inventory: List[Dict[str, str]] = []

class OnboardingData(UserUpdate, UserPreferencesUpdate, UserNutritionUpdate):
    """Combined schema for user onboarding"""
    pass


class UserResponse(BaseModel):
    """Response schema for user data"""
    success: bool = True
    user: User
