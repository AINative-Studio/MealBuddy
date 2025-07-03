from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, List

from app.db.base import get_db
from app.models.user import User
from app.api.v1.deps import get_current_active_user
from app.services.meal_planner.plan_generator import generate_meal_plan, swap_meal, shift_meal_plan, suggest_leftover_recipes

router = APIRouter()

class MealSwapRequest(BaseModel):
    day: str
    meal_type: str

class MealShiftRequest(BaseModel):
    days_to_shift: int

@router.get("/meal-plan")
async def get_meal_plan(
    current_user: User = Depends(get_current_active_user),
):
    """
    Generate a meal plan for the current user.
    """
    meal_plan = await generate_meal_plan(current_user)
    return meal_plan

@router.post("/meal-plan/swap")
async def swap_meal_endpoint(
    swap_request: MealSwapRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Swap a meal in the current user's meal plan.
    """
    # In a real application, the meal plan would be stored in the database
    # and retrieved here. For now, we regenerate it.
    current_meal_plan = await generate_meal_plan(current_user)
    
    updated_meal_plan = await swap_meal(
        current_user, current_meal_plan, swap_request.day, swap_request.meal_type
    )
    return updated_meal_plan

@router.post("/meal-plan/shift")
async def shift_meal_plan_endpoint(
    shift_request: MealShiftRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Shift the meal plan by a given number of days.
    """
    current_meal_plan = await generate_meal_plan(current_user)
    shifted_plan = await shift_meal_plan(current_user, current_meal_plan, shift_request.days_to_shift)
    return shifted_plan

@router.get("/meal-plan/leftovers")
async def get_leftover_suggestions(
    current_user: User = Depends(get_current_active_user),
) -> List[str]:
    """
    Get suggestions for recipes using leftovers.
    """
    suggestions = await suggest_leftover_recipes(current_user)
    return suggestions
