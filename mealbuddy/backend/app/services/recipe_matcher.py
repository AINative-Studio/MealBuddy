from typing import List, Dict, Any
from app.services.llama_service import generate_recipe_suggestions_with_llama

async def match_recipes_to_ingredients(ingredients: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Uses Llama service to generate recipe suggestions based on ingredients.
    """
    recipes = await generate_recipe_suggestions_with_llama(ingredients)
    return recipes