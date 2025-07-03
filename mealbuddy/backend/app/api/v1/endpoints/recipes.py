from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.api.v1.deps import get_current_active_user
from app.models.user import User
from app.services.recipe_matcher import match_recipes_to_ingredients

router = APIRouter()

@router.post("/recipes/match", response_model=List[Dict[str, Any]])
async def get_matching_recipes(
    ingredients: List[Dict[str, str]],
    current_user: User = Depends(get_current_active_user),
):
    """
    Get recipes that can be made with the given ingredients.
    """
    if not ingredients:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No ingredients provided.")
    
    recipes = await match_recipes_to_ingredients(ingredients)
    return recipes
