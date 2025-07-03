from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class RecipeFeedback(Base):
    """Recipe feedback model for user ratings and comments"""
    __tablename__ = "recipe_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False) # e.g., 1-5 stars
    comment = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")

    def __repr__(self):
        return f"<RecipeFeedback(id={self.id}, user_id={self.user_id}, recipe_name='{self.recipe_name}', rating={self.rating})>"
