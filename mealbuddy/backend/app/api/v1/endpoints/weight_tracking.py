from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.models.user import User
from app.models.user_weight_log import UserWeightLog
from app.schemas.user_weight_log import UserWeightLogCreate, UserWeightLogInDB
from app.api.v1.deps import get_current_active_user

router = APIRouter()

@router.post("/weight-log", response_model=UserWeightLogInDB)
async def log_user_weight(
    weight_log_in: UserWeightLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Log the current user's weight.
    """
    db_weight_log = UserWeightLog(
        **weight_log_in.dict(),
        user_id=current_user.id
    )
    db.add(db_weight_log)
    db.commit()
    db.refresh(db_weight_log)
    return db_weight_log

@router.get("/weight-log", response_model=List[UserWeightLogInDB])
async def get_user_weight_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get the current user's weight history.
    """
    weight_history = db.query(UserWeightLog).filter(UserWeightLog.user_id == current_user.id).order_by(UserWeightLog.logged_at).all()
    return weight_history
