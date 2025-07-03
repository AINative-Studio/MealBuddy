from pydantic import BaseModel

class NutritionData(BaseModel):
    calories: int
    protein: int
    carbs: int
    fat: int
