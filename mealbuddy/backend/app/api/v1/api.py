from fastapi import APIRouter

from app.api.v1.endpoints import auth, profile, meal_plans, nutrition, inventory, recipes, grocery_lists, shopping, feedback, weight_tracking

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(profile.router, prefix="/users", tags=["profile"])
api_router.include_router(meal_plans.router, prefix="/users", tags=["meal-plans"])
api_router.include_router(nutrition.router, prefix="/users", tags=["nutrition"])
api_router.include_router(inventory.router, prefix="/users", tags=["inventory"])
api_router.include_router(recipes.router, prefix="/users", tags=["recipes"])
api_router.include_router(grocery_lists.router, prefix="/users", tags=["grocery-lists"])
api_router.include_router(shopping.router, prefix="/users", tags=["shopping"])
api_router.include_router(feedback.router, prefix="/users", tags=["feedback"])
api_router.include_router(weight_tracking.router, prefix="/users", tags=["weight-tracking"])
