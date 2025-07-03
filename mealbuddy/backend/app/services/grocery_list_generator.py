from typing import List, Dict, Any

async def generate_grocery_list(meal_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dummy grocery list generation service.
    In a real application, this would parse the meal plan and generate a list of ingredients.
    """
    print(f"Simulating grocery list generation for meal plan: {meal_plan}")
    
    # For demonstration, return a static dummy grocery list
    grocery_items = [
        {"item": "chicken breast", "quantity": "1 kg", "estimated_price": 12.50},
        {"item": "salmon fillets", "quantity": "500g", "estimated_price": 15.00},
        {"item": "oats", "quantity": "1 box", "estimated_price": 4.00},
        {"item": "berries", "quantity": "200g", "estimated_price": 3.50},
        {"item": "spinach", "quantity": "1 bag", "estimated_price": 2.00},
        {"item": "quinoa", "quantity": "500g", "estimated_price": 6.00},
        {"item": "black beans", "quantity": "1 can", "estimated_price": 1.50},
        {"item": "corn", "quantity": "1 can", "estimated_price": 1.20},
        {"item": "tofu", "quantity": "1 block", "estimated_price": 3.00},
        {"item": "spaghetti", "quantity": "1 pack", "estimated_price": 2.50},
        {"item": "ground beef", "quantity": "500g", "estimated_price": 8.00},
        {"item": "avocado", "quantity": "2", "estimated_price": 4.00},
        {"item": "tuna", "quantity": "1 can", "estimated_price": 2.00},
        {"item": "bread", "quantity": "1 loaf", "estimated_price": 3.00},
        {"item": "pizza dough", "quantity": "1 pack", "estimated_price": 4.00},
        {"item": "cheese", "quantity": "200g", "estimated_price": 5.00},
        {"item": "eggs", "quantity": "1 dozen", "estimated_price": 4.50},
        {"item": "potatoes", "quantity": "1 kg", "estimated_price": 3.00},
        {"item": "carrots", "quantity": "500g", "estimated_price": 1.80},
    ]

    total_estimated_cost = sum(item["estimated_price"] for item in grocery_items)
    budget_optimization_message = ""

    # Simulate some budget optimization logic
    if total_estimated_cost > 50:
        budget_optimization_message = "Consider swapping some items for more budget-friendly alternatives to stay under $50."
    else:
        budget_optimization_message = "Your grocery list is budget-friendly!"

    return {
        "items": grocery_items,
        "total_estimated_cost": total_estimated_cost,
        "budget_optimization_message": budget_optimization_message
    }