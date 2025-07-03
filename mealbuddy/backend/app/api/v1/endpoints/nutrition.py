from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User, Goal, ActivityLevel
from app.api.v1.deps import get_current_active_user
from app.schemas.nutrition import NutritionData

router = APIRouter()

@router.get("/nutrition-dashboard", response_model=NutritionData)
async def get_nutrition_dashboard(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get nutrition dashboard data for the current user.
    """
    # This is a simplified estimation. In a real app, this would be calculated
    # based on the actual meal plan, recipe ingredients, and user's BMR/TDEE.
    calories = 2000
    protein = 150
    carbs = 200
    fat = 80

    if current_user.goal == Goal.BUILD_MUSCLE:
        calories += 300
        protein += 50
    elif current_user.goal == Goal.LOSE_WEIGHT:
        calories -= 500

    if current_user.activity_level == ActivityLevel.VERY_ACTIVE or current_user.activity_level == ActivityLevel.EXTRA_ACTIVE:
        calories += 400
    elif current_user.activity_level == ActivityLevel.SEDENTARY:
        calories -= 200

    return {
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat
    }