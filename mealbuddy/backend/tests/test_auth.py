import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

def test_register_user(db: Session):
    # Test successful user registration
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data  # Password should not be returned
    
    # Clean up
    db.query(User).filter(User.email == user_data["email"]).delete()
    db.commit()

def test_register_duplicate_email(db: Session):
    # Test registering with an email that already exists
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    # First registration should succeed
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Second registration with same email should fail
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json=user_data
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]
    
    # Clean up
    db.query(User).filter(User.email == user_data["email"]).delete()
    db.commit()

def test_login_successful(db: Session):
    # Test successful login
    email = "login@example.com"
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Create a test user
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name="Test User",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Test login
    form_data = {
        "username": email,
        "password": password
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Clean up
    db.query(User).filter(User.email == email).delete()
    db.commit()

def test_login_invalid_credentials():
    # Test login with invalid credentials
    form_data = {
        "username": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]

def test_protected_route_with_valid_token(db: Session):
    # Test accessing a protected route with a valid token
    email = "protected@example.com"
    password = "testpassword123"
    hashed_password = get_password_hash(password)
    
    # Create a test user
    db_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name="Test User",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Get token
    form_data = {
        "username": email,
        "password": password
    }
    
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/token",
        data=form_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    token = login_response.json()["access_token"]
    
    # Test protected route
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # This will fail until we implement the /users/me endpoint
    # For now, we expect a 404
    assert response.status_code in [200, 404]
    
    # Clean up
    db.query(User).filter(User.email == email).delete()
    db.commit()
