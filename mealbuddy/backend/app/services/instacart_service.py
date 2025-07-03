from typing import List, Dict, Any
import uuid
import asyncio

async def place_instacart_order(grocery_list: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Dummy Instacart service to simulate placing a grocery order.
    In a real application, this would involve actual API calls to Instacart.
    """
    print(f"Simulating Instacart order for: {grocery_list}")
    # Simulate network delay
    await asyncio.sleep(2)
    
    order_id = str(uuid.uuid4())
    estimated_delivery_time = "30-60 minutes"
    total_cost = sum(10 for _ in grocery_list) # Dummy cost

    return {
        "order_id": order_id,
        "status": "Order Placed",
        "estimated_delivery_time": estimated_delivery_time,
        "total_cost": f"${total_cost:.2f}",
        "message": "Your order has been placed with Instacart!"
    }
