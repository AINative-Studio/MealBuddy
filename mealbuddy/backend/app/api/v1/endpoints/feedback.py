from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.models.user import User
from app.models.recipe_feedback import RecipeFeedback
from app.schemas.recipe_feedback import RecipeFeedbackCreate, RecipeFeedbackInDB
from app.api.v1.deps import get_current_active_user

router = APIRouter()

@router.post("/recipe-feedback", response_model=RecipeFeedbackInDB)
async def submit_recipe_feedback(
    feedback_in: RecipeFeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Submit feedback (rating and optional comment) for a recipe.
    """
    db_feedback = RecipeFeedback(
        **feedback_in.dict(),
        user_id=current_user.id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/recipe-feedback", response_model=List[RecipeFeedbackInDB])
async def get_my_recipe_feedback(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get all recipe feedback submitted by the current user.
    """
    feedback = db.query(RecipeFeedback).filter(RecipeFeedback.user_id == current_user.id).all()
    return feedback
