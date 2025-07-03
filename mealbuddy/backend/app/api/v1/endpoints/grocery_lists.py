from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, PlainTextResponse
from typing import List, Dict, Any
import io

from app.api.v1.deps import get_current_active_user
from app.models.user import User
from app.services.grocery_list_generator import generate_grocery_list
from app.services.meal_planner.plan_generator import generate_meal_plan

router = APIRouter()

@router.get("/grocery-list", response_model=Dict[str, Any])
async def get_grocery_list(
    current_user: User = Depends(get_current_active_user),
):
    """
    Generate a grocery list based on the user's meal plan.
    """
    # For now, we'll generate a meal plan on the fly to create the grocery list.
    # In a real scenario, the meal plan would likely be stored and retrieved.
    meal_plan = await generate_meal_plan(current_user)
    grocery_list_data = await generate_grocery_list(meal_plan)
    return grocery_list_data

@router.get("/grocery-list/export/csv")
async def export_grocery_list_csv(
    current_user: User = Depends(get_current_active_user),
):
    """
    Export the grocery list as a CSV file.
    """
    meal_plan = await generate_meal_plan(current_user)
    grocery_list_data = await generate_grocery_list(meal_plan)
    
    output = io.StringIO()
    output.write("Item,Quantity,Estimated Price\n")
    for item in grocery_list_data["items"]:
        output.write(f"{item["item"]},{item["quantity"]},{item["estimated_price"]:.2f}\n")
    
    output.seek(0)
    
    headers = {
        "Content-Disposition": "attachment; filename=\"grocery_list.csv\""
    }
    return StreamingResponse(output, media_type="text/csv", headers=headers)

@router.get("/grocery-list/export/text")
async def export_grocery_list_text(
    current_user: User = Depends(get_current_active_user),
) -> PlainTextResponse:
    """
    Export the grocery list as plain text.
    """
    meal_plan = await generate_meal_plan(current_user)
    grocery_list_data = await generate_grocery_list(meal_plan)
    
    text_output = "Your Grocery List:\n\n"
    for item in grocery_list_data["items"]:
        text_output += f"- {item["item"]}: {item["quantity"]}\n"
    text_output += f"\nTotal Estimated Cost: ${grocery_list_data["total_estimated_cost"]:.2f}\n"
    if grocery_list_data["budget_optimization_message"]:
        text_output += f"\n{grocery_list_data["budget_optimization_message"]}\n"

    return PlainTextResponse(text_output)