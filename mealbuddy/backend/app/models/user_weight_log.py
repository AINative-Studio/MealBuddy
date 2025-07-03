from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class UserWeightLog(Base):
    """User weight log model to track historical weight data"""
    __tablename__ = "user_weight_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    weight_kg = Column(Float, nullable=False) # Weight in kilograms
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

    def __repr__(self):
        return f"<UserWeightLog(id={self.id}, user_id={self.user_id}, weight_kg={self.weight_kg}, logged_at={self.logged_at})>"
