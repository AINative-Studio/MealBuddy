from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RecipeFeedbackBase(BaseModel):
    recipe_name: str
    rating: int = Field(..., ge=1, le=5) # Rating between 1 and 5
    comment: Optional[str] = None

class RecipeFeedbackCreate(RecipeFeedbackBase):
    pass

class RecipeFeedbackInDB(RecipeFeedbackBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
