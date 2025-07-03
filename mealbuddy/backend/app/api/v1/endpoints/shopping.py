from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from app.api.v1.deps import get_current_active_user
from app.models.user import User
from app.services.grocery_list_generator import generate_grocery_list
from app.services.meal_planner.plan_generator import generate_meal_plan
from app.services.instacart_service import place_instacart_order

router = APIRouter()

@router.post("/shopping/instacart", response_model=Dict[str, Any])
async def order_with_instacart(
    current_user: User = Depends(get_current_active_user),
):
    """
    Place a grocery order with Instacart based on the generated grocery list.
    """
    # Generate meal plan and grocery list on the fly for the order
    meal_plan = await generate_meal_plan(current_user)
    grocery_list = await generate_grocery_list(meal_plan)

    if not grocery_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Grocery list is empty. Cannot place order.")

    order_details = await place_instacart_order(grocery_list)
    return order_details
