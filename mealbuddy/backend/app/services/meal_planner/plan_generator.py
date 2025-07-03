from app.models.user import User, Gender, ActivityLevel, Goal
from typing import Dict, Any, List
import random
from collections import deque
from app.services.llama_service import generate_text_with_llama
import json

async def generate_meal_plan(user: User) -> Dict[str, Any]:
    prompt = f"Generate a 7-day meal plan for a user with the following preferences: " \
             f"Dietary Restrictions: {user.dietary_restrictions}, " \
             f"Goal: {user.goal}, " \
             f"Activity Level: {user.activity_level}, " \
             f"Pantry Inventory: {user.pantry_inventory}. " \
             f"Please provide breakfast, lunch, and dinner for each day. " \
             f"Format the output as a JSON string with days as keys and meals as nested objects."

    # Call the Llama service to generate the meal plan text
    llama_response = await generate_text_with_llama(prompt, {
        "dietary_restrictions": user.dietary_restrictions,
        "goal": user.goal,
        "activity_level": user.activity_level,
        "pantry_inventory": user.pantry_inventory
    })

    # Attempt to parse the LLM response as JSON
    try:
        meal_plan = json.loads(llama_response)
        meal_plan["is_structured"] = True
        # Validate if the parsed JSON has the expected structure (optional but recommended)
        # For simplicity, we'll assume it's correctly structured if it parses as JSON.
        # If not, the frontend might break or display unexpected data.
    except json.JSONDecodeError:
        # If LLM does not return valid JSON, return a simplified structure
        meal_plan = {
            "unstructured_plan_text": llama_response,
            "is_structured": False # Flag to indicate unstructured
        }

    return meal_plan

async def swap_meal(user: User, current_meal_plan: Dict[str, Any], day: str, meal_type: str) -> Dict[str, Any]:
    """
    Uses Llama to re-optimize the meal plan after a meal swap.
    """
    prompt = f"The user wants to swap the {meal_type} meal on {day}. The current meal plan is: {current_meal_plan}. " \
             f"Generate a new 7-day meal plan, re-optimizing it based on the user's preferences: " \
             f"Dietary Restrictions: {user.dietary_restrictions}, " \
             f"Goal: {user.goal}, " \
             f"Activity Level: {user.activity_level}, " \
             f"Pantry Inventory: {user.pantry_inventory}. " \
             f"Ensure the {meal_type} meal on {day} is different. " \
             f"Format the output as a JSON string with days as keys and meals as nested objects."

    llama_response = await generate_text_with_llama(prompt, {
        "dietary_restrictions": user.dietary_restrictions,
        "goal": user.goal,
        "activity_level": user.activity_level,
        "pantry_inventory": user.pantry_inventory
    })

    try:
        updated_meal_plan = json.loads(llama_response)
        updated_meal_plan["is_structured"] = True
    except json.JSONDecodeError:
        updated_meal_plan = {
            "unstructured_plan_text": llama_response,
            "is_structured": False
        }
    return updated_meal_plan

async def shift_meal_plan(user: User, current_meal_plan: Dict[str, Any], days_to_shift: int) -> Dict[str, Any]:
    """
    Uses Llama to re-optimize the meal plan after a shift.
    """
    prompt = f"The user wants to shift the meal plan by {days_to_shift} days. The current meal plan is: {current_meal_plan}. " \
             f"Generate a new 7-day meal plan, re-optimizing it based on the user's preferences: " \
             f"Dietary Restrictions: {user.dietary_restrictions}, " \
             f"Goal: {user.goal}, " \
             f"Activity Level: {user.activity_level}, " \
             f"Pantry Inventory: {user.pantry_inventory}. " \
             f"Format the output as a JSON string with days as keys and meals as nested objects."

    llama_response = await generate_text_with_llama(prompt, {
        "dietary_restrictions": user.dietary_restrictions,
        "goal": user.goal,
        "activity_level": user.activity_level,
        "pantry_inventory": user.pantry_inventory
    })

    try:
        shifted_plan = json.loads(llama_response)
        shifted_plan["is_structured"] = True
    except json.JSONDecodeError:
        shifted_plan = {
            "unstructured_plan_text": llama_response,
            "is_structured": False
        }
    return shifted_plan

async def suggest_leftover_recipes(user: User) -> List[str]:
    """
    Simulates suggesting recipes for leftovers.
    In a real application, this would analyze recent meals and pantry items.
    """
    # Dummy suggestions based on common leftovers
    suggestions = [
        "Leftover Chicken Tacos",
        "Stir-fry with leftover vegetables",
        "Pasta with leftover meat sauce",
        "Frittata with leftover cooked potatoes and veggies"
    ]
    return random.sample(suggestions, k=min(len(suggestions), 2)) # Suggest up to 2
