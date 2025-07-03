
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserPreferencesUpdate, UserNutritionUpdate, UserResponse
from app.api.v1.deps import get_current_active_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user's profile.
    """
    return {"success": True, "user": current_user}


@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user's profile.
    """
    user_data = user_in.dict(exclude_unset=True)
    for field, value in user_data.items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"success": True, "user": current_user}


@router.put("/profile/preferences", response_model=UserResponse)
async def update_user_preferences(
    preferences_in: UserPreferencesUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user's dietary preferences.
    """
    preferences_data = preferences_in.dict(exclude_unset=True)
    for field, value in preferences_data.items():
        setattr(current_user, field, value)
        
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"success": True, "user": current_user}


@router.put("/profile/nutrition", response_model=UserResponse)
async def update_user_nutrition(
    nutrition_in: UserNutritionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update current user's nutrition goals.
    """
    nutrition_data = nutrition_in.dict(exclude_unset=True)
    for field, value in nutrition_data.items():
        setattr(current_user, field, value)
        
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return {"success": True, "user": current_user}
