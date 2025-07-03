from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import date
from enum import Enum as PyEnum
from typing import Dict, List, Optional
from sqlalchemy import Date, Enum, Float
from sqlalchemy.dialects.postgresql import JSONB

class Gender(str, PyEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class ActivityLevel(str, PyEnum):
    SEDENTARY = "sedentary"  # Little or no exercise
    LIGHT = "light"  # Light exercise/sports 1-3 days/week
    MODERATE = "moderate"  # Moderate exercise 3-5 days/week
    VERY_ACTIVE = "very_active"  # Hard exercise 6-7 days/week
    EXTRA_ACTIVE = "extra_active"  # Very hard exercise & physical job


class Goal(str, PyEnum):
    LOSE_WEIGHT = "lose_weight"
    MAINTAIN_WEIGHT = "maintain_weight"
    GAIN_WEIGHT = "gain_weight"
    BUILD_MUSCLE = "build_muscle"
    IMPROVE_ENDURANCE = "improve_endurance"


class User(Base):
    """User model for authentication and profile information"""
    __tablename__ = "users"

    # Authentication fields
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True, nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    
    # Status flags
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    onboarding_completed = Column(Boolean(), default=False)
    
    # Email verification
    verification_token = Column(String, unique=True, nullable=True)
    verification_token_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Password reset
    reset_password_token = Column(String, unique=True, nullable=True)
    reset_password_token_expires = Column(DateTime(timezone=True), nullable=True)
    
    # Profile information
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Enum(Gender), nullable=True)
    height_cm = Column(Float, nullable=True)  # Height in centimeters
    weight_kg = Column(Float, nullable=True)  # Weight in kilograms
    activity_level = Column(Enum(ActivityLevel), nullable=True)
    goal = Column(Enum(Goal), nullable=True)
    
    # Dietary preferences
    dietary_restrictions = Column(JSONB, default=dict)  # e.g., {"vegetarian": true, "vegan": false, ...}
    allergies = Column(JSONB, default=list)  # List of allergies
    disliked_ingredients = Column(JSONB, default=list)  # List of disliked ingredients
    preferred_cuisines = Column(JSONB, default=list)  # List of preferred cuisines
    
    # Budget and nutrition goals
    weekly_budget_cents = Column(Integer, nullable=True)  # Weekly budget in cents
    target_daily_calories = Column(Integer, nullable=True)
    target_protein_g = Column(Integer, nullable=True)
    target_carbs_g = Column(Integer, nullable=True)
    target_fats_g = Column(Integer, nullable=True)

    # Inventory
    pantry_inventory = Column(JSONB, default=list) # List of confirmed inventory items
    
    # Tracking
    last_login = Column(DateTime(timezone=True), nullable=True)
    login_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class RefreshToken(Base):
    """Refresh token model for JWT refresh tokens"""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id})>"
