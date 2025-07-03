from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserWeightLogBase(BaseModel):
    weight_kg: float = Field(..., gt=0)

class UserWeightLogCreate(UserWeightLogBase):
    pass

class UserWeightLogInDB(UserWeightLogBase):
    id: int
    user_id: int
    logged_at: datetime

    class Config:
        orm_mode = True
