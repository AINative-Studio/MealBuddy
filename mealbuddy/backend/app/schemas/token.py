from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: List[str] = []

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    is_verified: bool = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "password": "securepassword123"
            }
        }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "new.email@example.com",
                "full_name": "New Name",
                "password": "newsecurepassword123"
            }
        }

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "is_verified": False,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }

class EmailSchema(BaseModel):
    email: EmailStr
    
class ResetPassword(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "reset_token_here",
                "new_password": "newsecurepassword123"
            }
        }
